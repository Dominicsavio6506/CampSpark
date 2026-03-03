from django.urls import path
from .views import mark_attendance
from . import views

urlpatterns = [
    path("api/attendance/", mark_attendance),
    path("api/attendance/", mark_attendance, name="mark_attendance"),
    path("mark/", views.mark_attendance, name="mark_attendance"),
    path("success/", views.attendance_success, name="attendance_success"),
    path("attendance/my/", views.student_attendance_view, name="student_attendance"),
    path("my-attendance/", views.student_attendance_view, name="my_attendance"),

]
