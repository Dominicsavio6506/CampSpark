from django.contrib import admin
from .models import Notification, NotificationTarget

admin.site.register(Notification)
admin.site.register(NotificationTarget)
