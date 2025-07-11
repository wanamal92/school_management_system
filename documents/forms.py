from django import forms
from django.core.exceptions import ValidationError
from .models import Document
import os
from datetime import date


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['user_type', 'teacher', 'student',
                  'document_type', 'document_file', 'expire_date']
        widgets = {
            'expire_date': forms.DateInput(attrs={'type': 'date'}),
        }
        # Custom validation for 'teacher' and 'student' to ensure only one is selected

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get('user_type')
        teacher = cleaned_data.get('teacher')
        student = cleaned_data.get('student')

        if user_type == 'teacher' and not teacher:
            raise ValidationError("Please select a teacher for this document.")
        if user_type == 'student' and not student:
            raise ValidationError("Please select a student for this document.")

        if user_type == 'teacher' and student:
            raise ValidationError(
                "A teacher cannot be associated with a student for this document.")
        if user_type == 'student' and teacher:
            raise ValidationError(
                "A student cannot be associated with a teacher for this document.")

        return cleaned_data

    # Custom validation for 'document_file' to ensure valid file types
    def clean_document_file(self):
        document_file = self.cleaned_data.get('document_file')

        if document_file:
            valid_extensions = ['pdf', 'docx', 'jpg', 'jpeg', 'png', 'doc']
            file_extension = document_file.name.split('.')[-1].lower()

            if file_extension not in valid_extensions:
                raise ValidationError(
                    "Invalid file format. Only PDF, DOCX, JPG, JPEG, PNG, and DOC are allowed.")

            if document_file.size > 10 * 1024 * 1024:  # Max file size: 10MB
                raise ValidationError("File size should not exceed 10MB.")

        return document_file

    # Custom validation for 'expire_date' to ensure it is a future date if needed
    def clean_expire_date(self):
        expire_date = self.cleaned_data.get('expire_date')

        if expire_date:
            if expire_date < date.today():
                raise ValidationError(
                    "The expiration date cannot be in the past.")

        return expire_date
