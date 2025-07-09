from django import forms
from .models import Student
from clases.models import Class
from guardians.models import Guardian


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'title', 'first_name', 'last_name', 'full_name', 'student_number', 'gender', 'telephone_number',
            'whatsapp_number', 'email', 'date_of_birth', 'class_level', 'guardian', 'address', 'profile_photo'
        ]
        class_level = forms.ModelChoiceField(
            queryset=Class.objects.all(), empty_label="Select Class")
        guardian = forms.ModelChoiceField(
            queryset=Guardian.objects.all(), empty_label="Select Guardian")

        # Exclude the user field, since it's set automatically by the signal
        exclude = ['user']
