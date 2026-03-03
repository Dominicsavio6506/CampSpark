from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from students.models import Student
from attendance.models import AttendanceRecord
from marks.models import Marks
from camp_fees.models import Fee
from notifications.models import NotificationTarget
from notes.models import Note
from scholarships.models import Scholarship
from .forms import StudentProfileForm
from academics.models import SmartTimetable
from datetime import datetime
from .models import Student
from .forms import StudentForm
from events.models import Event
from datetime import date

@login_required
def student_dashboard(request):
    student = Student.objects.filter(user=request.user).first()

    if not student:
        return render(request, "students/dashboard.html", {
            "student": None,
            "attendance_percent": 0,
            "marks": [],
            "total_due": 0,
            "notifications": [],
            "cgpa": 0,
            "gpa": 0,
            "rank": None,
            "top_students": [],
            "total_scholarship": 0,
        })

    # Attendance
    records = AttendanceRecord.objects.filter(student=student)
    total = records.count()
    present = records.filter(present=True).count()
    attendance_percent = round((present / total) * 100, 2) if total else 0

    #Time table
    today = datetime.today().strftime("%a").upper()

    today_timetable = SmartTimetable.objects.filter(
        day=today,
        department=student.department_fk,
        semester=student.semester
    ).order_by("timeslot__start_time")

    # Marks
    marks_qs = Marks.objects.filter(student=student)
    marks = []
    total_marks = 0

    for m in marks_qs:
        score = m.total
        total_marks += score

        if score >= 90:
            grade = "A+"
        elif score >= 75:
            grade = "A"
        elif score >= 60:
            grade = "B"
        elif score >= 45:
            grade = "C"
        else:
            grade = "F"

        marks.append({
            "subject": m.subject,
            "score": score,
            "grade": grade
        })

    cgpa = round((total_marks / len(marks_qs)) / 10, 2) if marks_qs else 0
    gpa = cgpa

    # Rank
    rank = None
    top_students = []

    # Fees
    fee = Fee.objects.filter(student=student).first()
    total_due = fee.due_amount if fee else 0

    # Scholarship
    total_scholarship = sum(s.amount for s in Scholarship.objects.filter(student=student))

    # Notifications
    notifications = NotificationTarget.objects.filter(
        user=request.user
    ).select_related("notification").order_by(
        "-notification__created_at"
    )[:5]

    today_events = Event.objects.filter(
        date=date.today()
    )

    context = {
        "student": student,
        "attendance_percent": attendance_percent,
        "marks": marks,
        "cgpa": cgpa,
        "gpa": gpa,
        "rank": rank,
        "top_students": top_students,
        "total_due": total_due,
        "total_scholarship": total_scholarship,
        "notifications": notifications,
        "today_timetable": today_timetable,
        "today_events": today_events,

    }

    return render(request, "students/dashboard.html", context)

@login_required
def student_profile(request):
    student = Student.objects.filter(user=request.user).first()

    if not student:
        return render(request, "students/profile.html", {
            "error": "Student profile not found"
        })

    if request.method == "POST":
        form = StudentProfileForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
    else:
        form = StudentProfileForm(instance=student)

    return render(request, "students/profile.html", {
        "form": form,
        "student": student
    })

@login_required
def student_attendance(request):
    student = Student.objects.filter(user=request.user).first()

    if not student:
        return render(request, "students/attendance.html", {
            "error": "Student profile not found"
        })

    records = AttendanceRecord.objects.filter(student=student)

    total = records.count()
    present = records.filter(present=True).count()
    attendance_percent = round((present / total) * 100, 2) if total else 0

    context = {
        "student": student,
        "records": records,
        "attendance_percent": attendance_percent,
        "total_classes": total,
        "present_classes": present
    }

    return render(request, "students/attendance.html", context)

@login_required
def student_certificates(request):
    student = Student.objects.filter(user=request.user).first()

    if not student:
        return render(request, "students/certificates.html", {
            "error": "Student profile not found"
        })

    return render(request, "students/certificates.html", {
        "student": student
    })


@login_required
def student_profile(request):
    student = request.user.student

    return render(request, "students/profile.html", {
        "student": student
    })
