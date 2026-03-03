from django.db import models
from django.contrib.auth.models import User

DEPARTMENT_CHOICES = [
    ('Tamil', 'Tamil'),
    ('English', 'English'),
    ('Computer Science', 'Computer Science'),
    ('Physics', 'Physics'),
    ('Commerce', 'Commerce'),
]

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    subject = models.CharField(max_length=100, blank=True)
    is_hod = models.BooleanField(default=False)
    phone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        role = "HOD" if self.is_hod else "Faculty"
        return f"{self.name} ({role} - {self.department})"
