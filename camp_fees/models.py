from django.db import models
from students.models import Student
from decimal import Decimal

class Fee(models.Model):
    STATUS_CHOICES = [
        ('Paid', 'Paid'),
        ('Pending', 'Pending'),
        ('Overdue', 'Overdue'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    due_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    last_updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Prevent paid amount exceeding total fee
        if self.paid_amount > self.total_amount:
            self.paid_amount = self.total_amount

        # Calculate due safely
        self.due_amount = self.total_amount - self.paid_amount

        # Never allow negative due
        if self.due_amount < 0:
            self.due_amount = 0

        # Update status
        if self.due_amount == 0:
            self.status = "Paid"
        else:
            self.status = "Pending"

        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.student.name} - ₹{self.total_amount}"


class FeePayment(models.Model):
    fee = models.ForeignKey(Fee, on_delete=models.CASCADE, related_name="payments")
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=50, default="Cash")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        new_paid = self.fee.paid_amount + self.amount_paid

        if new_paid > self.fee.total_amount:
            new_paid = self.fee.total_amount

        self.fee.paid_amount = new_paid
        self.fee.save()

    def __str__(self):
        return f"{self.fee.student.name} - ₹{self.amount_paid}"

class Scholarship(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="fee_scholarships"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.CharField(max_length=255, default="Merit Scholarship")
    applied_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        fee = Fee.objects.filter(student=self.student).first()
        if fee:
            fee.total_amount = max(0, fee.total_amount - self.amount)
            fee.save()


    def __str__(self):
        return f"{self.student.name} - ₹{self.amount}"
