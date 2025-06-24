from django import forms
from .models import Class
from teachers.models import Teacher
from sections.models import Section

class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['class_name', 'class_code', 'section', 'class_in_charge']

    class_in_charge = forms.ModelChoiceField(queryset=Teacher.objects.all(), empty_label="Select Teacher")
    section = forms.ModelChoiceField(queryset=Section.objects.all(), empty_label="Select Section")
