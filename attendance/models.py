from django.db import models
from camp_staff.models import Staff
from students.models import Student
from datetime import date
from django.contrib.auth.models import User

class Attendance(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(default=date.today)
    student_name = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, default="Present")

    def __str__(self):
        return f"{self.student_name} - {self.date}"


class AttendanceRecord(models.Model):
    attendance = models.ForeignKey(
        Attendance,
        on_delete=models.CASCADE,
        related_name='records'
    )
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    present = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.name} - {'Present' if self.present else 'Absent'}"
