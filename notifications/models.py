from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    CATEGORY_CHOICES = [
        ('exam', 'Exam'),
        ('fee', 'Fee'),
        ('attendance', 'Attendance'),
        ('general', 'General'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
    ]

    title = models.CharField(max_length=200)
    message = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    target_role = models.CharField(max_length=20, default="all")
    expires_at = models.DateTimeField(null=True, blank=True)



    def __str__(self):
        return self.title


class NotificationTarget(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.notification.title}"
