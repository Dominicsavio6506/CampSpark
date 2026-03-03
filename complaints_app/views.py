from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import Complaint
from django.db.models import Count
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from special_roles.utils import is_role
from django.shortcuts import redirect, get_object_or_404

@csrf_exempt
def submit_complaint(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))

            title = data.get("title", "").strip()
            description = data.get("description", "").strip()

            if not title or not description:
                return JsonResponse({"error": "Missing fields"}, status=400)

            Complaint.objects.create(
                category=title,
                urgency="Normal",
                department=description,
                is_anonymous=True,
                status="Pending"
            )

            return JsonResponse({"message": "Complaint saved successfully"}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid method"}, status=405)

def complaint_ai_privacy_analyzer(request):
    total = Complaint.objects.count()

    category_stats = Complaint.objects.values("category").annotate(count=Count("category"))
    urgency_stats = Complaint.objects.values("urgency").annotate(count=Count("urgency"))
    department_stats = Complaint.objects.values("department").annotate(count=Count("department"))

    data = {
        "total_complaints": total,
        "category_stats": list(category_stats),
        "urgency_stats": list(urgency_stats),
        "department_stats": list(department_stats),
        "privacy_note": "AI analyzed metadata only. Complaint text was NOT accessed."
    }

    return JsonResponse(data)


def complaint_stats(request):
    total = Complaint.objects.count()

    category_stats = list(
        Complaint.objects.values("category")
        .annotate(count=Count("category"))
    )

    urgency_stats = list(
        Complaint.objects.values("urgency")
        .annotate(count=Count("urgency"))
    )

    department_stats = list(
        Complaint.objects.values("department")
        .annotate(count=Count("department"))
    )

    return JsonResponse({
        "total_complaints": total,
        "category_stats": category_stats,
        "urgency_stats": urgency_stats,
        "department_stats": department_stats,
        "privacy_note": "AI analyzed metadata only. Complaint text was NOT accessed."
    })

def complaint_form_page(request):
    return render(request, "complaints/form.html")

def complaint_list_page(request):
    data = Complaint.objects.all()
    return render(request, "complaints/list.html", {"data": data})

@login_required
def view_complaints(request):

    if not (request.user.is_staff or is_role(request, 'COMP')):
        return render(request, 'no_access.html')

    # normal logic here
    complaints = Complaint.objects.all() 
    return render(request, 'complaints/view.html', {
        'complaints': complaints
    })

@login_required
def update_status(request, complaint_id):

    if not (request.user.is_staff or is_role(request, 'COMP')):
        return render(request, 'no_access.html')

    complaint = get_object_or_404(Complaint, id=complaint_id)

    if request.method == "POST":
        new_status = request.POST.get("status")
        complaint.status = new_status
        complaint.save()

    return redirect('view_complaints')