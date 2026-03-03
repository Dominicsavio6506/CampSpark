from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.http import HttpResponse
import csv
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors

def all_events(request):
    upcoming = Event.objects.filter(date__gte=now().date()).order_by('date')
    past = Event.objects.filter(date__lt=now().date()).order_by('-date')

    return render(request, "events/all_events.html", {
        "upcoming": upcoming,
        "past": past,
    })

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    deadline_passed = False

    if event.registration_deadline_date and event.registration_deadline_time:
        deadline_datetime = datetime.combine(
            event.registration_deadline_date,
            event.registration_deadline_time
        )
        deadline_passed = datetime.now() > deadline_datetime

    participants = EventRegistration.objects.filter(event=event)
    participants_list = participants.select_related('student__student')

    already_registered = False
    if request.user.is_authenticated:
        already_registered = participants.filter(student=request.user).exists()

    is_admin = request.user.is_superuser

    is_incharge = EventStaffIncharge.objects.filter(
        event=event,
        staff=request.user
    ).exists()

    can_view_participants = is_admin or is_incharge

    can_register = (
        request.user.is_authenticated
        and not is_admin
        and not is_incharge
    )

    return render(request, "events/event_detail.html", {
        "event": event,
        "participants_count": participants.count(),
        "already_registered": already_registered,
        "staff_incharges": EventStaffIncharge.objects.filter(event=event),
        "student_heads": EventStudentHead.objects.filter(event=event),
        "participants_list": participants_list,
        "can_view_participants": can_view_participants,
        "deadline_passed": deadline_passed,
        "can_register": can_register,
    })

@login_required
def register_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.user.is_superuser or EventStaffIncharge.objects.filter(
        staff=request.user
    ).exists():
        return HttpResponse("Not allowed", status=403)

    deadline_passed = False
    if event.registration_deadline_date and event.registration_deadline_time:
        deadline_datetime = datetime.combine(
            event.registration_deadline_date,
            event.registration_deadline_time
        )
        deadline_passed = datetime.now() > deadline_datetime

    if deadline_passed:
        return redirect('event_detail', event_id=event.id)

    EventRegistration.objects.get_or_create(
        event=event,
        student=request.user
    )

    return redirect('event_detail', event_id=event.id)

@login_required
def cancel_registration(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    EventRegistration.objects.filter(
        event=event,
        student=request.user
    ).delete()

    return redirect('event_detail', event_id=event.id)

@login_required
def my_events(request):
    my_events = Event.objects.filter(
        eventstaffincharge__staff=request.user
    ).distinct()

    return render(request, "events/my_events.html", {
        "my_events": my_events
    })

@login_required
def download_report(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # deadline check
    deadline_passed = False
    if event.registration_deadline_date and event.registration_deadline_time:
        deadline_datetime = datetime.combine(
            event.registration_deadline_date,
            event.registration_deadline_time
        )
        deadline_passed = datetime.now() > deadline_datetime

    if not deadline_passed:
        return HttpResponse("Registration still open", status=403)

    registrations = EventRegistration.objects.filter(event=event)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{event.title}_report.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    y = height - 50

    # Title
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, y, f"Event Report - {event.title}")
    y -= 30

    # -------- TABLE DATA --------
    data = [["S.No", "Name", "Department", "Year"]]

    for i, r in enumerate(registrations, start=1):
        student = r.student.student
        data.append([
            str(i),
            student.name,
            student.department_fk.name,
            f"Year {student.year}"
        ])

    # -------- CREATE TABLE --------
    table = Table(data, colWidths=[40, 130, 190, 180])

    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("GRID", (0,0), (-1,-1), 1, colors.black),
    ]))

    table.wrapOn(p, width, height)
    table.drawOn(p, 40, y - (20 * len(data)))

    p.save()
    return response