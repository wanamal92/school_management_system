from django import forms
from .models import Class
from teachers.models import Teacher

class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['class_name', 'class_code', 'section', 'teacher_in_charge']

    teacher_in_charge = forms.ModelChoiceField(queryset=Teacher.objects.all(), empty_label="Select Teacher")
