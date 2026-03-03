from django.shortcuts import render, redirect, get_object_or_404
from .models import Asset, AssetIssue
from .forms import AssetForm, AssetIssueForm
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required


# special role check
def is_maintenance(user):
    return user.groups.filter(name="Maintenance").exists()


# ---------------- ASSET LIST ----------------
@login_required
def asset_list(request):
    assets = Asset.objects.all()
    return render(request, 'assets/list.html', {'assets': assets})


# ---------------- ADD ASSET ----------------
@login_required
def add_asset(request):

    if not request.user.is_superuser:
        return redirect("dashboard")

    form = AssetForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('asset_list')

    return render(request, 'assets/add.html', {'form': form})


# ---------------- REPORT ISSUE ----------------
@login_required
def report_issue(request):

    if not (request.user.is_staff or request.user.is_superuser):
        return redirect("dashboard")

    form = AssetIssueForm(request.POST or None)

    if form.is_valid():
        issue = form.save(commit=False)
        issue.reported_by = request.user
        issue.save()

        # decrease working quantity
        asset = issue.asset
        if asset.working_quantity > 0:
            asset.working_quantity -= 1
            asset.save()

        return redirect('asset_list')

    return render(request, 'assets/report.html', {'form': form})


# ---------------- ISSUE LIST ----------------
@login_required
def issue_list(request):

    if not (request.user.is_superuser or is_maintenance(request.user)):
        return redirect("dashboard")

    issues = AssetIssue.objects.all()
    return render(request, 'assets/issues.html', {'issues': issues})


# ---------------- UPDATE ISSUE STATUS ----------------
@login_required
def update_issue_status(request, issue_id, status):

    if not (request.user.is_superuser or is_maintenance(request.user)):
        return redirect("dashboard")

    issue = get_object_or_404(AssetIssue, id=issue_id)

    issue.status = status

    # if completed -> increase working quantity
    if status == "completed":
        issue.resolved_at = now()

        asset = issue.asset
        asset.working_quantity += 1
        asset.save()

    issue.save()

    return redirect("issue_list")