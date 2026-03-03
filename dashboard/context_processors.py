from .models import Reminder

def reminder_count(request):
    if request.user.is_authenticated:
        return {
            "reminder_count": Reminder.objects.filter(
                user=request.user,
                is_read=False
            ).count()
        }
    return {"reminder_count": 0}
