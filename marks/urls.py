from django.urls import path
from .views import (
    student_marks,
    exam_results,
    student_gpa,
    rank_list,
    download_report
)

urlpatterns = [
    path("student-marks/", student_marks, name="student_marks"),
    path("exam-results/", exam_results, name="exam_results"),
    path("gpa/", student_gpa, name="student_gpa"),
    path("rank-list/", rank_list, name="rank_list"),
    path("download-report/", download_report, name="download_report"),
]
