from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Staff
from students.models import Student
from marks.models import Marks
from notes.models import Note
from academics.models import Timetable, Exam
from special_roles.models import UserSpecialRole
from ai_assistant.views import (
    detect_weak_students,
    detect_attendance_risk,
    generate_staff_ai_insight,
    predict_student_performance,
    generate_study_recommendations,
    detect_fee_risk_students
)


@login_required
def staff_dashboard(request):
    staff = Staff.objects.filter(user=request.user).first()

    if not staff:
        return render(request, "staff/error.html", {"msg": "Staff profile not created yet"})

    students = Student.objects.filter(department_fk__name=staff.department)
    marks = Marks.objects.filter(student__department=staff.department)
    notes = Note.objects.all()

    weak_students = detect_weak_students()
    attendance_risk = detect_attendance_risk()
    ai_insight = generate_staff_ai_insight()
    performance_predictions = predict_student_performance()
    study_recommendations = generate_study_recommendations()
    fee_risk_students = detect_fee_risk_students()
    staff_role = UserSpecialRole.objects.filter(user=request.user).first()
    ai_message = f"""
    Students: {students.count()}
    Marks Recorded: {marks.count()}
    Weak Students: {len(weak_students)}
    Attendance Risk: {len(attendance_risk)}
    """

    return render(request, "staff/dashboard.html", {
        "staff": staff,
        "students": students,
        "marks": marks,
        "notes": notes,
        "ai_message": ai_message,
        "weak_students": weak_students,
        "attendance_risk": attendance_risk,
        "ai_insight": ai_insight,
        "performance_predictions": performance_predictions,
        "study_recommendations": study_recommendations,
        "fee_risk_students": fee_risk_students,
        "staff_role": staff_role
    })  


@login_required
def staff_students(request):
    staff = Staff.objects.filter(user=request.user).first()
    if not staff:
        return render(request, "staff/error.html", {"msg": "Staff profile missing"})

    students = Student.objects.filter(department_fk__name=staff.department)
    return render(request, "staff/students.html", {"students": students})


@login_required
def staff_marks(request):
    staff = Staff.objects.filter(user=request.user).first()
    if not staff:
        return render(request, "staff/error.html", {"msg": "Staff profile missing"})

    marks = Marks.objects.filter(student__department=staff.department)
    return render(request, "staff/marks.html", {"marks": marks})


@login_required
def staff_notes(request):

    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]

        Note.objects.create(
            title=title,
            content=content
        )

    notes = Note.objects.all()

    return render(request, "staff/notes.html", {"notes": notes})


@login_required
def staff_ai(request):
    return render(request, "staff/ai_report.html")


@login_required
def upload_marks(request):
    students = Student.objects.all()
    q = request.GET.get("q")
    dept = request.GET.get("dept")
    year = request.GET.get("year")

    if q:
        students = students.filter(name__icontains=q)

    if dept:
        students = students.filter(department=dept)

    if year:
        students = students.filter(year=year)


    if request.method == "POST":
        student = Student.objects.get(id=request.POST["student"])
        subject = request.POST["subject"]

        internal = int(request.POST.get("internal", 0))
        semester = int(request.POST.get("semester", 0))

        Marks.objects.create(
            student=student,
            subject=subject,
            internal_mark=internal,
            semester_mark=semester
        )

    return render(request, "staff/upload_marks.html", {"students": students})


@login_required
def staff_timetable(request):
    timetable = Timetable.objects.all()
    return render(request, "staff/timetable.html", {"timetable": timetable})


@login_required
def upload_exam_marks(request):
    students = Student.objects.all()
    exams = Exam.objects.all()

    if request.method == "POST":
        student = Student.objects.get(id=request.POST["student"])
        exam = Exam.objects.get(id=request.POST["exam"])
        subject = request.POST["subject"]

        internal = int(request.POST.get("internal", 0))
        semester = int(request.POST.get("semester", 0))

        Marks.objects.create(
            student=student,
            exam=exam,
            subject=subject,
            internal_mark=internal,
            semester_mark=semester
        )

    return render(request, "staff/upload_exam_marks.html", {
        "students": students,
        "exams": exams
    })


@login_required
def exam_results(request):
    student = Student.objects.filter(user=request.user).first()

    if not student:
        return render(request, "marks/error.html", {
            "msg": "Student account not linked"
        })

    marks = Marks.objects.filter(student=student)

    return render(request, "marks/exam_results.html", {
        "student": student,
        "marks": marks
    })