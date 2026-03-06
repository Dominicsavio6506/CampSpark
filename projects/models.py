from django.db import models
from django.conf import settings
from students.models import Student
from academics.models import Department

# ==========================
# MAIN PROJECT MODEL
# ==========================
class Project(models.Model):

    STATUS_CHOICES = [
        ('ONGOING', 'Ongoing'),
        ('COMPLETED', 'Completed'),
        ('ARCHIVE', 'Archive'),
    ]

    title = models.CharField(max_length=255)
    team_name = models.CharField(max_length=150)

    department = models.ForeignKey(
        'Department',
        on_delete=models.SET_NULL,
        null=True
    )
    domain = models.CharField(max_length=100, blank=True)

    abstract = models.TextField()
    technology_used = models.TextField(blank=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_projects'
    )

    guide_staff = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='guided_projects'
    )

    year = models.IntegerField(default=3)

    deadline = models.DateField(null=True, blank=True)

    edit_count = models.IntegerField(default=0)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='ONGOING'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def auto_archive(self):
        if self.status == "COMPLETED":
            self.status = "ARCHIVE"
            self.save()


# ==========================
# TEAM MEMBERS
# ==========================
class ProjectMember(models.Model):

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='members'
    )

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    is_leader = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student} - {self.project}"


# ==========================
# PROGRESS STEPS
# ==========================
class ProjectProgress(models.Model):

    STEP_CHOICES = [
        ('IDEA', 'Idea Submitted'),
        ('PROPOSAL', 'Proposal Approved'),
        ('PHASE1', 'Phase 1 Complete'),
        ('PHASE2', 'Phase 2 Complete'),
        ('FINAL', 'Final Submission'),
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='progress'
    )

    step_name = models.CharField(max_length=20, choices=STEP_CHOICES)
    description = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    approved_by_staff = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.project} - {self.step_name}"


# ==========================
# FINAL PROJECT MEDIA
# ==========================
class ProjectMedia(models.Model):

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='media'
    )

    image = models.ImageField(upload_to='project_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.project.title

# ==========================
# STAFF STUDENT ASSIGNMENT
# ==========================
class StaffStudentAssignment(models.Model):

    staff = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="assigned_students"
    )

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="staff_guides"
    )

    def __str__(self):
        return f"{self.staff} -> {self.student}"

class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
