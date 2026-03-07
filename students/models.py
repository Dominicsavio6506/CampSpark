from django.db import models
from django.contrib.auth.models import User
from academics.models import Course, Semester

# Department Model
class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=50, unique=True)

    department = models.CharField(max_length=100)
    department_fk = models.ForeignKey(
        'academics.Department',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    year = models.IntegerField()

    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    photo = models.ImageField(upload_to="student_photos/", null=True, blank=True)

    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    blood_group = models.CharField(max_length=10, null=True, blank=True)
    aadhaar = models.CharField(max_length=20, null=True, blank=True)
    religion = models.CharField(max_length=50, null=True, blank=True)
    community = models.CharField(max_length=50, null=True, blank=True)
    nationality = models.CharField(max_length=50, null=True, blank=True)
    emergency_contact = models.CharField(max_length=15, null=True, blank=True)

    father_name = models.CharField(max_length=100, null=True, blank=True)
    parent_phone = models.CharField(max_length=15, null=True, blank=True)
    parent_occupation = models.CharField(max_length=100, null=True, blank=True)
    annual_income = models.CharField(max_length=50, null=True, blank=True)
    hostel_status = models.CharField(max_length=20, null=True, blank=True)

    certificate_10th = models.FileField(upload_to="certificates/", null=True, blank=True)
    certificate_12th = models.FileField(upload_to="certificates/", null=True, blank=True)
    certificate_degree = models.FileField(upload_to="certificates/", null=True, blank=True)
    community_certificate = models.FileField(upload_to="certificates/", null=True, blank=True)
    income_certificate = models.FileField(upload_to="certificates/", null=True, blank=True)
    id_proof = models.FileField(upload_to="certificates/", null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    semester = models.ForeignKey(Semester, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
