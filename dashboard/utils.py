from .models import Reminder
from attendance.models import AttendanceRecord
from fees.models import Fee

def generate_student_reminders(user):
    student = user.student

    # ---------- ATTENDANCE CALCULATION ----------
    total_records = AttendanceRecord.objects.filter(student=student).count()
    present_records = AttendanceRecord.objects.filter(
        student=student,
        present=True
    ).count()

    if total_records > 0:
        attendance_percent = (present_records / total_records) * 100
    else:
        attendance_percent = 100

    if attendance_percent < 75:
        Reminder.objects.get_or_create(
            user=user,
            title="Low Attendance",
            message=f"Your attendance is {int(attendance_percent)}%",
            color="red"
        )

    # ---------- FEE DUE CHECK ----------
    fee = Fee.objects.filter(student=student).order_by('-created_at').first()

    if fee and fee.due_amount > 0:
        Reminder.objects.get_or_create(
            user=user,
            title="Fee Pending",
            message=f"Due Amount ₹{fee.due_amount}",
            color="yellow"
        )

def get_today_focus_student(user):
    student = user.student

    # ---------- ATTENDANCE ----------
    total = AttendanceRecord.objects.filter(student=student).count()
    present = AttendanceRecord.objects.filter(
        student=student,
        present=True
    ).count()

    if total > 0:
        attendance_percent = int((present / total) * 100)
    else:
        attendance_percent = 100

    # ---------- FEES ----------
    fee = Fee.objects.filter(student=student).order_by('-created_at').first()
    due = fee.due_amount if fee else 0

    return {
        "attendance": attendance_percent,
        "fee_due": due
    }

def get_color(value, type):
    if type == "attendance":
        if value < 60:
            return "red"
        elif value < 75:
            return "yellow"
        else:
            return "green"

    if type == "fee":
        if value > 0:
            return "red"
        return "green"

def get_suggestion(attendance, fee_due):
    if attendance < 75:
        return "Improve attendance by attending more classes."
    if fee_due > 0:
        return "Pay your pending fees soon."
    return "All good! Keep maintaining this performance."
