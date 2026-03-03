from .models import Notification, NotificationTarget

def send_attendance_alert(student_user, percentage):
    if percentage < 75:
        exists = NotificationTarget.objects.filter(
            user=student_user,
            notification__category="attendance",
            is_read=False
        ).exists()

        if exists:
            return

        notif = Notification.objects.create( 
            title="Attendance Alert",
            message=f"Your attendance is {percentage}%. Minimum required is 75%.",
            category="attendance",
            priority="high"
        )
        NotificationTarget.objects.create(
            notification=notif,
            user=student_user
        )

def send_fee_due_alert(user, due_amount):
    if due_amount > 0:
        exists = NotificationTarget.objects.filter(
            user=user,
            notification__category="fee",
            is_read=False
        ).exists()

        if exists:
            return

        notif = Notification.objects.create(
            title="Fee Due Reminder",
            message=f"₹{due_amount} pending. Please pay soon.",
            category="fee",
            priority="high"
        )
        NotificationTarget.objects.create(notification=notif, user=user)

