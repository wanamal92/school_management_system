# forms.py
from django import forms
from .models import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['user_type','teacher', 'student', 'document_type', 'document_file', 'expire_date']
        widgets = {
            'expire_date': forms.DateInput(attrs={'type': 'date'}),
        }
