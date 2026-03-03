from django.db import models

class Complaint(models.Model):
    category = models.CharField(max_length=100)
    urgency = models.CharField(max_length=50)
    department = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    is_anonymous = models.BooleanField(default=True)
    status = models.CharField(default="Pending", max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} | {self.urgency}"
