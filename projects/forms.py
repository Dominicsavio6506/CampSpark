from django import forms
from .models import Project


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = [
            'title',
            'team_name',
            'department',
            'domain',
            'abstract',
            'technology_used',
        ]