from django import forms
from .models import Section

class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['section_name', 'section_code']

    
