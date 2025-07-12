from django import forms
from .models import Duty, TeacherDuty
from teachers.models import Teacher
from django.core.exceptions import ValidationError
import re

# Form for creating/updating Duty


class DutyForm(forms.ModelForm):
    class Meta:
        model = Duty
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

        # Custom validation for 'name'
    def clean_name(self):
        name = self.cleaned_data.get('name')

        # Ensure the duty name is not empty
        if not name:
            raise ValidationError("Duty name cannot be empty.")

        # Ensure that the duty name contains only letters, numbers, and spaces
        if not re.match("^[a-zA-Z0-9\s]*$", name):
            raise ValidationError("Duty name must only contain letters, numbers, and spaces.")

        # Ensure the name is unique (if it already exists, raise an error)
        if Duty.objects.exclude(id=self.instance.id).filter(name=name).exists():
            raise ValidationError(f"The duty '{name}' already exists. Please choose a different name.")
        
        return name

# Form for creating/updating TeacherDuty


class TeacherDutyForm(forms.ModelForm):
    class Meta:
        model = TeacherDuty
        fields = ['teacher', 'duty', 'year']

    year = forms.ChoiceField(
        choices=[(str(year), str(year)) for year in range(2025, 2050)])
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

        # Custom validation for 'teacher'
    def clean_teacher(self):
        teacher = self.cleaned_data.get('teacher')
        if not Teacher.objects.filter(id=teacher.id).exists():
            raise ValidationError("The selected teacher does not exist.")
        return teacher

    # Custom validation for 'duty'
    def clean_duty(self):
        duty = self.cleaned_data.get('duty')
        if not Duty.objects.filter(id=duty.id).exists():
            raise ValidationError("The selected duty does not exist.")
        return duty

    # Custom validation for 'year' to ensure it is within the range
    def clean_year(self):
        year = self.cleaned_data.get('year')
        year = int(year)

        # Ensure year is within the valid range
        if year < 1980 or year > 2050:
            raise ValidationError("Year must be between 1980 and 2050.")
        
        # Check for uniqueness
        teacher = self.cleaned_data.get('teacher')
        duty = self.cleaned_data.get('duty')

        if TeacherDuty.objects.exclude(id=self.instance.id).filter(teacher=teacher, duty=duty, year=year).exists():
            raise ValidationError(f"This teacher already has this duty assigned in the year {year}.")
        
        return year
