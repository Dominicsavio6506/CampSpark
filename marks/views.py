from django.shortcuts import render
from .models import Marks
from students.models import Student
from django.contrib.auth.decorators import login_required
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse

@login_required
def student_marks(request):
    student = Student.objects.filter(user=request.user).first()

    if not student:
        return render(request, "marks/student_marks.html", {"error": "Student not linked"})

    marks = Marks.objects.filter(student=student)

    return render(request, "marks/student_marks.html", {"marks": marks, "student": student})

@login_required
def exam_results(request):
    student = Student.objects.filter(user=request.user).first()
    marks = Marks.objects.filter(student=student)

    return render(request, "marks/exam_results.html", {"marks": marks})

@login_required
def student_gpa(request):
    student = Student.objects.filter(user=request.user).first()
    marks = Marks.objects.filter(student=student)

    if not marks.exists():
        return render(request, "marks/gpa.html", {"error": "No marks found"})

    total_points = sum(m.grade_point() for m in marks)
    gpa = round(total_points / marks.count(), 2)

    return render(request, "marks/gpa.html", {
        "student": student,
        "marks": marks,
        "gpa": gpa
    })

def rank_list(request):
    students = Student.objects.all()
    rank_data = []

    for s in students:
        marks = Marks.objects.filter(student=s)
        if marks.exists():
            avg = sum(m.total for m in marks) / marks.count()
            rank_data.append((s, avg))

    rank_data.sort(key=lambda x: x[1], reverse=True)

    return render(request, "marks/rank_list.html", {"rank_data": rank_data})

def download_report(request):
    student = Student.objects.filter(user=request.user).first()
    marks = Marks.objects.filter(student=student)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report_card.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    p.drawString(50, 750, f"Report Card — {student.name}")

    y = 720
    for m in marks:
        p.drawString(50, y, f"{m.subject}: {m.total} ({m.grade()})")
        y -= 20

    p.save()
    return response