# forms.py
from django import forms
from .models import Qualification, TeacherQualification


class QualificationForm(forms.ModelForm):
    class Meta:
        model = Qualification
        fields = ['name', 'short_code']


class TeacherQualificationForm(forms.ModelForm):
    class Meta:
        model = TeacherQualification
        fields = ['teacher', 'qualification', 'institute', 'date_obtained']

        widgets = {
            'date_obtained': forms.DateInput(attrs={'type': 'date'}),

        }

    def clean(self):
        cleaned_data = super().clean()
        teacher = cleaned_data.get("teacher")
        qualification = cleaned_data.get("qualification")

        if teacher and qualification:
            # Check if the teacher already has this qualification
            if TeacherQualification.objects.filter(teacher=teacher, qualification=qualification).exists():
                raise forms.ValidationError(
                    "This teacher already has this qualification.")
        return cleaned_data
