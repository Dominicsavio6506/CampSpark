from django.urls import path
from . import views

urlpatterns = [
    path('', views.special_dashboard, name='special_dashboard'),
    path('library/', views.library_panel, name='library_panel'),
    path('nss/', views.nss_panel, name='nss_panel'),
    path('complaint/', views.complaint_panel, name='complaint_panel'),
    path('nss/add/', views.nss_add_participation, name='nss_add'),
    path("nss/delete/<int:id>/", views.nss_delete, name="nss_delete"),
    path("nss/download/", views.nss_download_pdf, name="nss_download"),
]