from django import forms
from django.contrib.auth.models import User
from .models import LabSchedule, DisciplineCase, NSSEventParticipation

class LabScheduleForm(forms.ModelForm):
    class Meta:
        model = LabSchedule
        fields = ["day", "start_time", "end_time", "class_name"]


class DisciplineCaseForm(forms.ModelForm):
    class Meta:
        model = DisciplineCase
        fields = ["student", "reason", "severity"]


class NSSParticipationForm(forms.ModelForm):
    students = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(is_staff=False),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = NSSEventParticipation
        fields = ["students"]