from django.forms import ModelForm
from .models import Asset, AssetIssue

class AssetForm(ModelForm):
    class Meta:
        model = Asset
        fields = [
            'name',
            'category',
            'department',
            'location',
            'total_quantity',
            'working_quantity',
        ]

class AssetIssueForm(ModelForm):
    class Meta:
        model = AssetIssue
        fields = ['asset','issue_text','priority']