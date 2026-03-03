from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.models import Notification


class Event(models.Model):
    EVENT_TYPES = [
        ('Workshop', 'Workshop'),
        ('Seminar', 'Seminar'),
        ('Cultural', 'Cultural'),
        ('Sports', 'Sports'),
        ('Technical', 'Technical'),
        ('Department', 'Department Event'),
    ]

    title = models.CharField(max_length=200)
    type = models.CharField(max_length=50, choices=EVENT_TYPES)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    registration_deadline_date = models.DateField(null=True, blank=True)
    registration_deadline_time = models.TimeField(null=True, blank=True)
    place = models.CharField(max_length=200)
    rules = models.TextField(blank=True)
    max_participants = models.IntegerField()

    def __str__(self):
        return self.title


class EventStaffIncharge(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    staff = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.event} - {self.staff}"


class EventStudentHead(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.event} - {self.student}"


class EventRegistration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('event', 'student')  # 🔥 duplicate protection

    def __str__(self):
        return f"{self.student} -> {self.event}"

@receiver(post_save, sender=Event)
def create_event_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            title=f"📢 New Event Added: {instance.title}",
            message=f"Event on {instance.date}"
        ) 