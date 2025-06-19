from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        # Exclude the user field, since it's set automatically by the signal
        exclude = ['user']
