from django.urls import path
from .views import student_timetable

urlpatterns = [
    path("student/timetable/", student_timetable, name="student_timetable"),
]
