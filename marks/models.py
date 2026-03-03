from django.db import models
from students.models import Student
from camp_staff.models import Staff

class Marks(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    exam = models.ForeignKey("academics.Exam", on_delete=models.CASCADE, null=True, blank=True)
    internal_mark = models.IntegerField(default=0)
    semester_mark = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    graded_by = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def grade(self):
        if self.total >= 90: return "A"
        elif self.total >= 75: return "B"
        elif self.total >= 60: return "C"
        elif self.total >= 50: return "D"
        return "F"

    def save(self, *args, **kwargs):
        self.total = (self.internal_mark or 0) + (self.semester_mark or 0)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.name} - {self.subject} - {self.total}"
