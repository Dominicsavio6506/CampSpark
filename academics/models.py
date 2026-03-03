from django.db import models
from django.contrib.auth.models import User

class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Semester(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    number = models.IntegerField()

    def __str__(self):
        return f"{self.course.name} - Sem {self.number}"


class Subject(models.Model):
    name = models.CharField(max_length=100)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    credits = models.IntegerField()

    def __str__(self):
        return self.name


class FacultySubjectAssign(models.Model):
    faculty = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.faculty.username} → {self.subject.name}"

class Timetable(models.Model):
    course = models.CharField(max_length=100)
    day = models.CharField(max_length=20)
    subject = models.CharField(max_length=100)
    faculty = models.CharField(max_length=100)
    time = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.day} - {self.subject}"

class Exam(models.Model):
    name = models.CharField(max_length=100)
    exam_date = models.DateField()
    course = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# ===== TIMETABLE SMART MODELS =====

DAYS = [
    ("MON", "Monday"),
    ("TUE", "Tuesday"),
    ("WED", "Wednesday"),
    ("THU", "Thursday"),
    ("FRI", "Friday"),
    ("SAT", "Saturday"),
]

class TimeSlot(models.Model):
    slot_name = models.CharField(max_length=20)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_break = models.BooleanField(default=False)

    def __str__(self):
        return self.slot_name


class Classroom(models.Model):
    room_no = models.CharField(max_length=10)
    block = models.CharField(max_length=20)
    capacity = models.IntegerField()

    def __str__(self):
        return f"{self.block}-{self.room_no}"


class SmartTimetable(models.Model):
    day = models.CharField(max_length=3, choices=DAYS)

    department = models.ForeignKey("academics.Department", on_delete=models.CASCADE)
    semester = models.ForeignKey("academics.Semester", on_delete=models.CASCADE)
    section = models.CharField(max_length=5)

    subject = models.ForeignKey("academics.Subject", on_delete=models.CASCADE)
    faculty = models.ForeignKey("auth.User", on_delete=models.CASCADE)

    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)

    class Meta:
        unique_together = [
            ("day", "department", "semester", "section", "timeslot"),
            ("day", "faculty", "timeslot"),
            ("day", "classroom", "timeslot"),
        ]

    def __str__(self):
        return f"{self.day} - {self.subject}"
