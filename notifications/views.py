from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Notification, NotificationTarget
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q


@login_required
def my_notifications(request):
    notifications = NotificationTarget.objects.filter(
        user=request.user
    ).filter(
        Q(notification__expires_at__isnull=True) |
        Q(notification__expires_at__gte=timezone.now())
    ).select_related("notification").order_by("-notification__created_at")

    return render(request, "notifications/list.html", {
        "notifications": notifications
    })



@login_required
def mark_as_read(request, notif_id):
    notif = NotificationTarget.objects.get(
        id=notif_id,
        user=request.user
    )
    notif.is_read = True
    notif.read_at = timezone.now()
    notif.save()

    return redirect('my_notifications')

def is_admin(user):
    return user.is_staff

@login_required
@user_passes_test(is_admin)
def send_notification(request):
    if request.method == 'POST':
        title = request.POST['title']
        message = request.POST['message']
        category = request.POST['category']
        priority = request.POST['priority']

        notif = Notification.objects.create(
            title=title,
            message=message,
            category=category,
            priority=priority,
            sender=request.user
        )

        users = User.objects.all()
        NotificationTarget.objects.bulk_create([
            NotificationTarget(notification=notif, user=u)
            for u in users
        ])

        return redirect('/notifications/')

    return render(request, 'notifications/send.html')

def unread_count(request):  
    if request.user.is_authenticated:
        return {
            "unread_notifications": NotificationTarget.objects.filter(
                user=request.user,
                is_read=False
            ).count()
        }
    return {"unread_notifications": 0}
