from django.shortcuts import render
from .models import SmartTimetable, TimeSlot
from students.models import Student
from django.contrib.auth.decorators import login_required

@login_required
def student_timetable(request):
    student = Student.objects.filter(user=request.user).first()

    if not student:
        return render(request, "academics/student_timetable.html", {
            "table": {},
            "slots": [],
            "days": [],
        })

    slots = TimeSlot.objects.all().order_by("start_time")
    days = ["MON", "TUE", "WED", "THU", "FRI", "SAT"]


    table = {}

    for slot in slots:
        table[slot] = {}
        for day in days:
            entry = SmartTimetable.objects.filter(
                day=day,
                department_id=student.department_fk_id,
                semester_id=student.semester_id,
                timeslot_id=slot.id
            ).first()

            table[slot][day] = entry

    return render(request, "academics/student_timetable.html", {
        "table": table,
        "slots": slots,
        "days": days
    })
