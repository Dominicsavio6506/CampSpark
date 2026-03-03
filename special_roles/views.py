from django.shortcuts import render, redirect
from .utils import is_role
from django.contrib.auth.models import User
from .models import NSSEventParticipation
from events.models import Event
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import csv
from reportlab.pdfgen import canvas
from django.shortcuts import get_object_or_404
from reportlab.lib.pagesizes import A4


# =============================
# SPECIAL DASHBOARD
# =============================
@login_required
def special_dashboard(request):
    return render(request, "special_roles/dashboard.html")



# =============================
# LIBRARY PANEL
# =============================
@login_required
def library_panel(request):
    if not is_role(request, "LIB"):
        return render(request, "no_access.html")
    return render(request, "special_roles/library.html")

# =============================
# COMPLAINT PANEL
# =============================
@login_required
def complaint_panel(request):
    if not is_role(request, "COMP"):
        return render(request, "no_access.html")

    return render(request, "special_roles/complaint.html")

# =============================
# NSS PANEL (MAIN)
# =============================
@login_required
def nss_panel(request):

    if not is_role(request, "NSS"):
        return render(request, "no_access.html")

    data = NSSEventParticipation.objects.all()

    return render(
        request,
        "special_roles/nss.html",
        {"data": data}
    )


@login_required
def nss_add_participation(request):

    if not is_role(request, "NSS"):
        return render(request, "no_access.html")

    if request.method == "POST":

        NSSEventParticipation.objects.create(
            student_name=request.POST.get("student_name"),
            department=request.POST.get("department"),
            year=request.POST.get("year"),
            created_by=request.user
        )

        return redirect("nss_panel")

    return render(request, "special_roles/nss_add.html")

@login_required
def nss_delete(request, id):

    if not is_role(request, "NSS"):
        return render(request, "no_access.html")

    obj = get_object_or_404(NSSEventParticipation, id=id)
    obj.delete()

    return redirect("nss_panel")

# =============================
# NSS REPORT DOWNLOAD
# =============================
@login_required
def nss_download_pdf(request):

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="nss_list.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # HEADER
    p.setFont("Helvetica-Bold", 16)
    p.drawString(180, height-50, "NSS Participation List")

    # TABLE HEADER
    p.setFont("Helvetica-Bold", 10)

    y = height - 100

    p.drawString(50, y, "S.No")
    p.drawString(100, y, "Student Name")
    p.drawString(250, y, "Department")
    p.drawString(400, y, "Year")

    y -= 20

    records = NSSEventParticipation.objects.all()

    p.setFont("Helvetica", 10)

    i = 1
    for r in records:

        p.drawString(50, y, str(i))
        p.drawString(100, y, r.student_name)
        p.drawString(250, y, r.department)
        p.drawString(400, y, r.year)

        y -= 20
        i += 1

        # new page
        if y < 50:
            p.showPage()
            y = height - 50

    p.save()
    return response