from django.urls import path
from .views import (
    staff_dashboard,
    staff_students,
    staff_marks,
    staff_notes,
    staff_ai,
    upload_marks,
    staff_timetable,
    upload_exam_marks
)

urlpatterns = [
    path("", staff_dashboard, name="staff_dashboard"),

    path("students/", staff_students, name="staff_students"),
    path("marks/", staff_marks, name="staff_marks"),
    path("notes/", staff_notes, name="staff_notes"),
    path("ai/", staff_ai, name="staff_ai"),

    path("upload-marks/", upload_marks, name="upload_marks"),
    path("upload-exam-marks/", upload_exam_marks, name="upload_exam_marks"),

    path("timetable/", staff_timetable, name="staff_timetable"),
]
