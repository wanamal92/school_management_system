from django import forms
from .models import Prefect
from students.models import Student
from clases.models import Class
from django.core.exceptions import ValidationError
from datetime import date


class PrefectForm(forms.ModelForm):
    class Meta:
        model = Prefect
        fields = ['student', 'prefect_type', 'class_level', 'year']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'prefect_type': forms.Select(attrs={'class': 'form-control'}),
            'class_level': forms.Select(attrs={'class': 'form-control'}),
            'year': forms.Select(attrs={'class': 'form-control'})  # Ensure 'year' field is a dropdown
        }

    def __init__(self, *args, **kwargs):
        super(PrefectForm, self).__init__(*args, **kwargs)
        
        # Add a dynamic range of years for selection
        current_year = date.today().year
        year_choices = [(str(year), str(year)) for year in range(current_year, current_year + 20)]  # Current year to next 20 years
        self.fields['year'] = forms.ChoiceField(choices=year_choices, widget=forms.Select(attrs={'class': 'form-control'}))

        if self.data:
            prefect_type = self.data.get('prefect_type')
            if prefect_type == 'Class Monitor':
                self.fields['class_level'].required = True
            else:
                self.fields['class_level'].required = False
        else:
            self.fields['class_level'].required = False

    # Clean the 'year' field to validate
    def clean_year(self):
        year = self.cleaned_data.get('year')
        if not year:
            raise ValidationError("Year is required.")

        # Ensure the year is within a valid range
        year = int(year)
        if year < 1980 or year > 2050:
            raise ValidationError("Year must be between 1980 and 2050.")
        
        return year

    def clean(self):
        cleaned_data = super().clean()
        prefect_type = cleaned_data.get('prefect_type')
        class_level = cleaned_data.get('class_level')
        student = cleaned_data.get('student')
        year = cleaned_data.get('year')

        if prefect_type == 'Class Monitor' and not class_level:
            self.add_error('class_level', 'Class level is required for Class Monitor.')

        if prefect_type != 'Class Monitor':
            cleaned_data['class_level'] = None

        # Check if a Prefect with the same student and year already exists
        if Prefect.objects.exclude(id=self.instance.id).filter(student=student, year=year).exists():
            raise ValidationError(f"This student already has a prefect role assigned for the year {year}.")

        return cleaned_data


