from django.db import models
from django.contrib.auth.models import User
from events.models import Event

ROLE_CHOICES = [
    ('HOD', 'HOD'),
    ('LAB', 'Lab In-Charge'),
    ('LIB', 'Library Admin'),
    ('DISC', 'Discipline Officer'),
    ('NSS', 'NSS Officer'),
    ('COMP', 'Complaint Committee'),
]


class UserSpecialRole(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.role}"



# ===============================
# NSS PARTICIPATION
# ===============================
class NSSEventParticipation(models.Model):

    student_name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    year = models.CharField(max_length=20)

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.student_name} - NSS"