from django.db import models
from students.models import Student


class Fee(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="student_fees_new"
    )
    total_amount = models.FloatField()
    paid_amount = models.FloatField()
    due_amount = models.FloatField()
    status = models.CharField(max_length=20, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} — Due ₹{self.due_amount}"
