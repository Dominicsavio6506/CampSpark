from django.db import models
from django.contrib.auth.models import User

class Location(models.Model):
    building = models.CharField(max_length=100)
    room = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.building} - {self.room}"

class Asset(models.Model):

    STATUS_CHOICES = [
        ('working','Working'),
        ('repair','Under Repair'),
        ('damaged','Damaged'),
        ('lost','Lost'),
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    total_quantity = models.IntegerField()
    working_quantity = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='working')
    created_at = models.DateTimeField(auto_now_add=True)

    LAB_CHOICES = [
        ("GENERAL", "General"),
        ("LAB", "Lab Equipment"),
    ]

    scope = models.CharField(
        max_length=20,
        choices=LAB_CHOICES,
        default="GENERAL"
    )

    @property
    def not_working(self):
        return self.total_quantity - self.working_quantity

    def __str__(self):
        return self.name


class AssetIssue(models.Model):

    PRIORITY = [
        ('low','Low'),
        ('medium','Medium'),
        ('high','High'),
    ]

    STATUS = [
        ('open','Open'),
        ('repair','Under Repair'),
        ('completed','Completed'),
    ]

    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    issue_text = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20,choices=STATUS,default='open')