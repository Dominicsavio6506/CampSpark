from django.urls import path
from . import views

urlpatterns = [
    path("my/", views.student_scholarships, name="student_scholarships"),
]
