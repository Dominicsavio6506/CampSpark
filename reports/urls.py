from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='reports_dashboard'),
    path('student-pdf/', views.student_pdf, name='student_pdf'),

    path('attendance-pdf/', views.attendance_pdf, name='attendance_pdf'),
    path('fees-pdf/', views.fees_pdf, name='fees_pdf'),    
    path('marks-pdf/', views.marks_pdf, name='marks_pdf'),
    path('excel-report/', views.excel_report, name='excel_report'),
    path('semester-result/<int:student_id>/', views.semester_result_pdf, name='semester_result_pdf'),
    path('bonafide/<int:student_id>/', views.bonafide_pdf, name='bonafide_pdf'),
    path('fee-certificate/<int:student_id>/', views.fee_certificate_pdf, name='fee_certificate_pdf'),
    path('attendance-full/', views.attendance_full_pdf, name='attendance_full_pdf'),



]
