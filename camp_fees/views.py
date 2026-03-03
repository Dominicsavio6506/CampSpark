from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from students.models import Student
from .models import Fee, FeePayment
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from notifications.utils import send_fee_due_alert

@login_required
def my_fees(request):
    student = Student.objects.filter(user=request.user).first()
    fee = Fee.objects.filter(student=student).first()
    payments = FeePayment.objects.filter(fee=fee)

    # ✅ AUTO ALERT HERE (CORRECT DATA SOURCE)
    if fee:
        send_fee_due_alert(student.user, fee.due_amount)

    return render(request, "fees/my_fees.html", {
        "fee": fee,
        "payments": payments
    })

@login_required
def download_fee_receipt(request):
    student = Student.objects.filter(user=request.user).first()
    fee = Fee.objects.filter(student=student).first()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="fee_receipt.pdf"'

    p = canvas.Canvas(response)
    p.setFont("Helvetica", 12)

    p.drawString(100, 750, "CampSpark Fee Receipt")
    p.drawString(100, 720, f"Student: {student.name}")
    p.drawString(100, 700, f"Total Fee: ₹{fee.total_amount}")
    p.drawString(100, 680, f"Paid: ₹{fee.paid_amount}")
    p.drawString(100, 660, f"Due: ₹{fee.due_amount}")
    p.drawString(100, 640, f"Status: {fee.status}")

    p.save()
    return response

