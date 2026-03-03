from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login

from students.models import Student
from camp_staff.models import Staff
from marks.models import Marks

from ai_assistant.views import detect_complaint_patterns
from ai_assistant.views import detect_dropout_risk
from ai_assistant.views import detect_burnout_risk
from ai_assistant.views import detect_placement_readiness
from ai_assistant.views import detect_top_students
from ai_assistant.views import generate_smart_campus_insight
from adminpanel.models import ActivityLog
from complaints_app.models import Complaint


def home(request):
    return render(request, "home.html")


@login_required
def student_dashboard(request):
    logs = ActivityLog.objects.order_by("-created_at")[:10]

    return render(request, "students/dashboard.html", {
        "logs": logs
    })


@login_required
def staff_dashboard(request):
    logs = ActivityLog.objects.order_by("-created_at")[:10]

    return render(request, "staff/dashboard.html", {
        "logs": logs
    })



@login_required
def admin_dashboard(request):
    total_students = Student.objects.count()
    total_staff = Staff.objects.count()
    total_marks = Marks.objects.count()
    complaint_count = Complaint.objects.count()

    complaint_ai = detect_complaint_patterns()
    dropout_risk = detect_dropout_risk()
    burnout_risk = detect_burnout_risk()
    placement_readiness = detect_placement_readiness()
    top_students = detect_top_students()
    smart_insight = generate_smart_campus_insight()

    logs = ActivityLog.objects.order_by("-created_at")[:10]

    ai_summary = f"{total_students} students, {total_staff} staff, {total_marks} marks recorded."

    context = {
        "total_students": total_students,
        "total_staff": total_staff,
        "total_marks": total_marks,
        "total_complaints": complaint_count,  
        "marks": Marks.objects.all(),
        "ai_summary": ai_summary,
        "complaint_ai": complaint_ai,
        "dropout_risk": dropout_risk,
        "burnout_risk": burnout_risk,
        "placement_readiness": placement_readiness,
        "top_students": top_students,
        "smart_insight": smart_insight,
        "logs": logs,
    }

    return render(request, "adminpanel/dashboard.html", context)


@login_required
def dashboard_router(request):
    user = request.user

    if user.is_superuser:
        return redirect("/admin-panel/")

    if user.is_staff:
        return redirect("/staff/")

    return redirect("/student/")


def logout_view(request):
    logout(request)
    return redirect("/login/")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("/dashboard/")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("/dashboard/")

        return render(request, "login.html", {
            "error": "Invalid username or password"
        })

    return render(request, "login.html")