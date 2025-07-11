# forms.py
from django import forms
from .models import Qualification, TeacherQualification
from django.core.exceptions import ValidationError


class QualificationForm(forms.ModelForm):
    class Meta:
        model = Qualification
        fields = ['name', 'short_code']
    
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field in self.fields.values():
                field.widget.attrs['class'] = 'form-control'
    # Custom validation for 'name' to ensure uniqueness
    def clean_name(self):
        name = self.cleaned_data.get('name')

        # Ensure that the name is not empty
        if not name:
            raise ValidationError("Qualification name cannot be empty.")
        
        # Ensure the name is unique
        if Qualification.objects.filter(name=name).exists():
            raise ValidationError(f"The qualification name '{name}' already exists. Please choose a different name.")
        
        return name

    # Custom validation for 'short_code' to ensure uniqueness
    def clean_short_code(self):
        short_code = self.cleaned_data.get('short_code')

        # Ensure that the short code is not empty
        if not short_code:
            raise ValidationError("Short code cannot be empty.")
        
        # Ensure the short code is unique
        if Qualification.objects.filter(short_code=short_code).exists():
            raise ValidationError(f"The short code '{short_code}' already exists. Please choose a different short code.")
        
        return short_code


class TeacherQualificationForm(forms.ModelForm):
    class Meta:
        model = TeacherQualification
        fields = ['teacher', 'qualification', 'institute', 'date_obtained']

    

        widgets = {
            'date_obtained': forms.DateInput(attrs={'type': 'date'}),

        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    # Custom validation for the 'institute' field
    def clean_institute(self):
        institute = self.cleaned_data.get('institute')

        if not institute:
            raise ValidationError("Institute name cannot be empty.")
        
        if len(institute) > 255:
            raise ValidationError("Institute name cannot exceed 255 characters.")
        
        return institute

    def clean(self):
        cleaned_data = super().clean()
        teacher = cleaned_data.get('teacher')
        qualification = cleaned_data.get('qualification')

        # Validate that a teacher cannot have the same qualification twice
        if teacher and qualification:
            if TeacherQualification.objects.filter(teacher=teacher, qualification=qualification).exists():
                raise ValidationError(
                    "This teacher already has this qualification.")

        # Validate that the date_obtained is not in the future
        date_obtained = cleaned_data.get('date_obtained')
        if date_obtained and date_obtained > forms.fields.DateField().to_python(str(forms.fields.DateField().now())):
            raise ValidationError("The date obtained cannot be in the future.")

        return cleaned_data
