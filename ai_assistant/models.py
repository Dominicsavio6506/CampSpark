from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class ChatHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_type = models.CharField(
        max_length=20,
        choices=[('student', 'Student'), ('staff', 'Staff'), ('admin', 'Admin')],
        default='staff'
    )
    message = models.TextField()
    reply = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} ({self.user_type}) - {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
