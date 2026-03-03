from django.db import models
from django.contrib.auth.models import User

class Reminder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    message = models.TextField()
    color = models.CharField(max_length=20, default="yellow")
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class DailyResetLog(models.Model):
    last_reset = models.DateField(auto_now=True)

class Event(models.Model):
    title = models.CharField(max_length=200)
    event_date = models.DateField()
    event_time = models.CharField(max_length=20)
    role = models.CharField(max_length=20, default="student")

    def __str__(self):
        return self.title