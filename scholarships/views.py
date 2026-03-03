from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from students.models import Student
from .models import Scholarship

@login_required
def student_scholarships(request):
    student = Student.objects.filter(user=request.user).first()
    scholarships = Scholarship.objects.filter(student=student)

    return render(request, "scholarships/student_scholarships.html", {
        "scholarships": scholarships
    })
