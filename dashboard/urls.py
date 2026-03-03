from django.urls import path
from . import views

urlpatterns = [
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('reminders/', views.reminders_page, name='reminders_page'),
    path('mark_read/<int:id>/', views.mark_read, name='mark_read'),
]
