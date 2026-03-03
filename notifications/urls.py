from django.urls import path
from . import views

urlpatterns = [
    path('', views.my_notifications, name='my_notifications'),
    path('read/<int:notif_id>/', views.mark_as_read, name='mark_as_read'),
    path('send/', views.send_notification, name='send_notification'),

]
