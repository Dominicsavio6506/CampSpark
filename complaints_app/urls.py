from django.urls import path
from .views import submit_complaint, complaint_ai_privacy_analyzer, complaint_stats, complaint_form_page, view_complaints
from . import views

urlpatterns = [
    path("api/complaints/", submit_complaint, name="submit_complaint"),
    path("api/complaint-ai-privacy/", complaint_ai_privacy_analyzer),
    path("api/complaints/stats/", complaint_stats, name="complaint_stats"),
    path("form/", complaint_form_page),
    path("view/", view_complaints, name="view_complaints"),
    path("update-status/<int:complaint_id>/", views.update_status, name="update_status"),


]
