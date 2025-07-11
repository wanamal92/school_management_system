from django import forms
from .models import Competition, CompetitionResult
from django.core.exceptions import ValidationError
import re

class CompetitionForm(forms.ModelForm):
    class Meta:
        model = Competition
        fields = ['name', 'competition_type']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    # Custom validation for 'name'
    def clean_name(self):
        name = self.cleaned_data.get('name')
        
        # Check if the competition name is empty
        if not name:
            raise ValidationError("Competition name cannot be empty.")
        
        # Check if the name contains only letters and spaces
        if not re.match("^[a-zA-Z\s]*$", name):
            raise ValidationError("Competition name must only contain letters and spaces.")
        
        return name

    # Custom validation for 'competition_type'
    def clean_competition_type(self):
        competition_type = self.cleaned_data.get('competition_type')

        # Check if the competition type is selected (not empty)
        if not competition_type:
            raise ValidationError("Competition type must be selected.")
        
        return competition_type


# Form for creating/updating CompetitionResult


class CompetitionResultForm(forms.ModelForm):
    class Meta:
        model = CompetitionResult
        fields = ['student', 'competition', 'year', 'result']

    year = forms.ChoiceField(
        choices=[(str(year), str(year)) for year in range(1980, 2050)])
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    # Custom validation for 'student'
    def clean_student(self):
        student = self.cleaned_data.get('student')
        # You can add further validations here if needed
        if not student:
            raise ValidationError("Student must be selected.")
        return student

    # Custom validation for 'competition'
    def clean_competition(self):
        competition = self.cleaned_data.get('competition')
        # Ensure a competition is selected
        if not competition:
            raise ValidationError("Competition must be selected.")
        return competition

    # Custom validation for 'year'
    def clean_year(self):
        year = self.cleaned_data.get('year')
        # Ensure the year is within the valid range (1980-2050)
        if not 1980 <= year <= 2050:
            raise ValidationError("Year must be between 1980 and 2050.")
        return year

    # Custom validation for 'result'
    def clean_result(self):
        result = self.cleaned_data.get('result')
        # Ensure that the result is selected
        if result not in dict(CompetitionResult._meta.get_field('result').choices):
            raise ValidationError("Please select a valid competition result.")
        return result
