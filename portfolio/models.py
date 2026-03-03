from django.db import models

class Portfolio(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    bio = models.TextField()
    skills = models.TextField()
    projects = models.TextField()
    resume = models.FileField(upload_to="resumes/", null=True, blank=True)

    def __str__(self):
        return self.name
