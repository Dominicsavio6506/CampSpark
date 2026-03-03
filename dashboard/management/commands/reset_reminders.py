from django.core.management.base import BaseCommand
from dashboard.models import Reminder

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        Reminder.objects.all().delete()
        print("Reminders reset complete")
