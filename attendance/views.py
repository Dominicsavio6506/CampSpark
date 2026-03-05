from django.shortcuts import render, redirect
from students.models import Student
from .models import Attendance, AttendanceRecord
from datetime import date
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from notifications.utils import send_attendance_alert


@login_required
def mark_attendance(request):
    students = Student.objects.all()

    if request.method == "POST":
        today = date.today()

        attendance = Attendance.objects.create(
            staff=request.user.staff if hasattr(request.user, "staff") else None,
            date=today
        )

        for student in students:
            present = request.POST.get(str(student.id)) == "on"

            AttendanceRecord.objects.create(
                attendance=attendance,
                student=student,
                present=present
            )

        return redirect("attendance_success")

    return render(request, "attendance/mark_attendance.html", {"students": students})


def attendance_success(request):
    return render(request, "attendance/success.html")

def student_attendance_view(request):
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        return render(request, "attendance/student_view.html", {
            "error": "Student account not linked. Contact admin."
        })

    records = AttendanceRecord.objects.filter(student=student)

    total = records.count()
    present = records.filter(present=True).count()
    percent = round((present / total) * 100, 2) if total > 0 else 0

    # ✅ AUTO ALERT HERE
    send_attendance_alert(student.user, percent)

    return render(request, "attendance/student_view.html", {
        "records": records,
        "total": total,
        "present": present,
        "percent": percent,
        "student": student
    })

@login_required
def my_attendance(request):
    student = Student.objects.filter().first()

    if not student:
        return render(request, "attendance/student_view.html", {
            "error": "No student records found in database."
        })

    records = AttendanceRecord.objects.filter(student=student)

    total = records.count()
    present = records.filter(present=True).count()
    percent = round((present / total) * 100, 2) if total > 0 else 0

    return render(request, "attendance/student_view.html", {
        "records": records,
        "percent": percent,
        "student": student
    })
