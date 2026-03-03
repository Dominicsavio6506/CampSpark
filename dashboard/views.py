from django.shortcuts import render
from django.shortcuts import redirect
from .models import Reminder
from .utils import (
    generate_student_reminders,
    get_today_focus_student,
    get_color
)
from .utils import get_suggestion
from django.shortcuts import get_object_or_404
from events.models import Event
from django.utils import timezone

def student_dashboard(request):
    generate_student_reminders(request.user)

    all_reminders = Reminder.objects.filter(user=request.user)
    unread_reminders = all_reminders.filter(is_read=False)

    focus = get_today_focus_student(request.user)

    today_events = Event.objects.filter(
        date=date.today()
    )

    print("TODAY DATE =", date.today())
    print("EVENTS =", today_events)

    upcoming_events = Event.objects.filter(
        date__gte=date.today()
    ).count()

    context = {
        "reminders": unread_reminders,
        "all_reminders": all_reminders,
        "focus": focus,
        "attendance_color": get_color(focus["attendance"], "attendance"),
        "fee_color": get_color(focus["fee_due"], "fee"),
        "today_events": today_events,
        "upcoming_events": upcoming_events,
        "suggestion": get_suggestion(
            focus["attendance"],
            focus["fee_due"]
        ),
    }

    return render(request, "dashboard/student_dashboard.html", context)


def reminders_page(request):
    reminders = Reminder.objects.filter(user=request.user)
    return render(request, "dashboard/reminders.html", {
        "reminders": reminders
    })

def mark_read(request, id):
    reminder = Reminder.objects.filter(
        id=id,
        user=request.user
    ).first()

    if reminder:
        reminder.is_read = True
        reminder.save()

    return redirect('reminders_page')

from django.shortcuts import render

def admin_dashboard(request):
    return render(request, 'adminpanel/dashboard.html')
