from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_events, name='all_events'),
    path('<int:event_id>/', views.event_detail, name='event_detail'),
    path('<int:event_id>/register/', views.register_event, name='register_event'),
    path('<int:event_id>/cancel/', views.cancel_registration, name='cancel_registration'),
    path("my/", views.my_events, name="my_events"),
    path('download-report/<int:event_id>/',
     views.download_report,
     name='download_report'),
]