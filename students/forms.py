from django import forms
from .models import Student

class StudentProfileForm(forms.ModelForm):

    certificate_10th = forms.FileField(required=False)
    certificate_12th = forms.FileField(required=False)
    certificate_degree = forms.FileField(required=False)
    community_certificate = forms.FileField(required=False)
    income_certificate = forms.FileField(required=False)
    id_proof = forms.FileField(required=False)

    class Meta:
        model = Student
        fields = [
            "phone",
            "address",
            "photo",

            "father_name",
            "parent_phone",
            "dob",
            "gender",
            "blood_group",
            "aadhaar",
            "community",
            "religion",
            "nationality",
            "parent_occupation",
            "annual_income",
            "emergency_contact",
            "hostel_status",

            "certificate_10th",
            "certificate_12th",
            "certificate_degree",
            "community_certificate",
            "income_certificate",
            "id_proof"
        ]

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = "__all__"