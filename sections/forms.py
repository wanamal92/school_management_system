from django import forms
from .models import Section
from django.core.exceptions import ValidationError


class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['section_name', 'section_code']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    # Custom validation for 'section_name'
    def clean_section_name(self):
        section_name = self.cleaned_data.get('section_name')

        # Ensure that section_name is not empty
        if not section_name:
            raise ValidationError("Section name cannot be empty.")
        
        # Ensure the section_name does not exceed 255 characters
        if len(section_name) > 255:
            raise ValidationError("Section name cannot exceed 255 characters.")
        
        return section_name

    # Custom validation for 'section_code'
    def clean_section_code(self):
        section_code = self.cleaned_data.get('section_code')

        # Ensure the section_code is unique
        if Section.objects.exclude(id=self.instance.id).filter(section_code=section_code).exists():
            raise ValidationError(f"The section code '{section_code}' is already taken. Please choose a different code.")
        
        # Ensure the section_code does not exceed 100 characters
        if len(section_code) > 100:
            raise ValidationError("Section code cannot exceed 100 characters.")
        
        return section_code
