from django.urls import path
from . import views

urlpatterns = [
    path("", views.student_dashboard, name="student_dashboard"),
    path("dashboard/", views.student_dashboard, name="student_dashboard"),
    path("profile/", views.student_profile, name="student_profile"),
    path("attendance/", views.student_attendance, name="student_attendance"),
    path("certificates/", views.student_certificates, name="student_certificates"),
    path("attendance/", views.student_attendance, name="student_attendance"),
    path('profile/', views.student_profile, name='student_profile'),

    
]
