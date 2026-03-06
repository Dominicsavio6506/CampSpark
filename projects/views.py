from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProjectForm
from .models import (
    Project,
    ProjectMember,
    StaffStudentAssignment,
    ProjectProgress
)
from students.models import Student
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth import get_user_model
User = get_user_model()


@login_required
def projects_home(request):

    context = {}

    if hasattr(request.user, "student"):
        context["role"] = "student"

    elif hasattr(request.user, "staff"):
        context["role"] = "staff"

    elif request.user.is_superuser:
        context["role"] = "admin"

    return render(request, "projects/projects_home.html", context)


# ==========================
# CREATE PROJECT (STUDENT)
# ==========================
@login_required
def create_project(request):

    if not hasattr(request.user, "student"):
        return redirect("home")

    # 🔥 CHECK if already created OR already member
    already_project = Project.objects.filter(
        created_by=request.user
    ).exists()

    already_member = ProjectMember.objects.filter(
        student=request.user
    ).exists()

    if already_project or already_member:

        project = Project.objects.filter(
            created_by=request.user
        ).first()

        if not project:
            member = ProjectMember.objects.filter(
                student=request.user
            ).first()
            project = member.project

        return render(request, "projects/already_created.html", {
            "project": project
        })

    form = ProjectForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():

            project = form.save(commit=False)
            project.created_by = request.user
            project.save()

            # auto leader create
            ProjectMember.objects.create(
                project=project,
                student=request.user,
                is_leader=True
            )

            return redirect("projects_home")

    return render(request, "projects/create_project.html", {
        "form": form
    })


# ==========================
# EDIT PROJECT
# ==========================
@login_required
def edit_project(request, project_id):

    project = get_object_or_404(Project, id=project_id)

    if project.created_by != request.user:
        return redirect("projects_home")

    if project.edit_count >= 3:
        return render(request, "projects/locked.html")

    if project.deadline and project.deadline < timezone.now().date():
        return render(request, "projects/locked.html")

    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.edit_count += 1
            obj.save()
            form.save_m2m()
            return redirect("project_detail", project_id=project.id)

    else:
        form = ProjectForm(instance=project)

    return render(request, "projects/create_project.html", {
        "form": form
    })


@login_required
def staff_panel(request):

    if not hasattr(request.user, "staff"):
        return redirect("home")

    projects = Project.objects.filter(
        guide_staff__isnull=True
    )

    return render(request, "projects/staff_panel.html", {
        "projects": projects
    })


# ==========================
# PROJECT DETAIL + ADD MEMBER
# ==========================
@login_required
def project_detail(request, project_id):

    project = get_object_or_404(Project, id=project_id)

    # ===== ADD MEMBER (POST) =====
    if request.method == "POST":
        student_id = request.POST.get("student")

        if student_id:

            # ❌ already in ANY project block
            already_any_project = ProjectMember.objects.filter(
                student_id=student_id
            ).exists()

            if not already_any_project:
                ProjectMember.objects.create(
                    project=project,
                    student_id=student_id
                )

        return redirect("project_detail", project_id=project.id)

    members = ProjectMember.objects.filter(project=project)

    # ✅ ONLY REAL STUDENTS
    students = User.objects.filter(
        is_staff=False,
        is_superuser=False
    ).exclude(
        id__in=ProjectMember.objects.values_list("student_id", flat=True)
    )

    progress = ProjectProgress.objects.filter(project=project)

    return render(request, "projects/project_detail.html", {
        "project": project,
        "members": members,
        "students": students,
        "progress": progress,
    })


@login_required
def remove_member(request, pk):
    member = get_object_or_404(ProjectMember, id=pk)

    # ❌ Leader delete block
    if member.is_leader:
        return redirect("project_detail", project_id=member.project.id)

    project_id = member.project.id
    member.delete()

    return redirect("project_detail", project_id=project_id)


@login_required
def archive_projects(request):
    projects = Project.objects.filter(status="ARCHIVE")
    return render(request, "projects/archive.html", {
        "projects": projects
    })


@login_required
def assign_project_to_staff(request, project_id):

    if not hasattr(request.user, "staff"):
        return redirect("home")

    project = Project.objects.get(id=project_id)

    if project.guide_staff:
        return redirect("staff_all")

    staff_count = Project.objects.filter(
        guide_staff=request.user
    ).count()

    if staff_count >= 5:
        return redirect("staff_all")

    project.guide_staff = request.user
    project.save()

    return redirect("staff_my")


@login_required
def staff_all_projects(request):

    projects = Project.objects.filter(status="ONGOING")

    return render(request, "projects/staff_all.html", {
        "projects": projects
    })


@login_required
def staff_my_projects(request):

    projects = Project.objects.filter(
        guide_staff=request.user
    )

    return render(request, "projects/staff_my.html", {
        "projects": projects
    })


@login_required
def manual_archive(request, project_id):

    if not request.user.is_superuser:
        return redirect("home")

    project = Project.objects.get(id=project_id)
    project.status = "ARCHIVE"
    project.save()

    return redirect("archive_projects")


@login_required
def admin_project_control(request):

    if not request.user.is_superuser:
        return redirect("home")

    projects = Project.objects.order_by("-created_at")

    return render(request, "projects/admin_control.html", {
        "projects": projects
    })


@login_required
def unassign_project(request, pk):
    project = get_object_or_404(Project, id=pk)
    project.guide_staff = None
    project.save()
    return redirect("staff_my")

@login_required
def add_progress(request, project_id):

    project = get_object_or_404(Project, id=project_id)

    # ❌ students cannot update
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect("project_detail", project_id=project.id)

    if request.method == "POST":
        step = request.POST.get("step_name")
        desc = request.POST.get("description", "")

        # duplicate step block
        already = ProjectProgress.objects.filter(
            project=project,
            step_name=step
        ).exists()

        if not already:
            ProjectProgress.objects.create(
                project=project,
                step_name=step,
                description=desc,
                approved_by_staff=True
            )

        return redirect("project_detail", project_id=project.id)

    return redirect("project_detail", project_id=project.id)