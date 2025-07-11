from django import forms
from .models import Prefect
from students.models import Student
from clases.models import Class
from django.core.exceptions import ValidationError


class PrefectForm(forms.ModelForm):
    class Meta:
        model = Prefect
        fields = ['student', 'prefect_type', 'class_level', 'year']

    
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'prefect_type': forms.Select(attrs={'class': 'form-control'}),
            'class_level': forms.Select(attrs={'class': 'form-control'}),
            'year': forms.Select(attrs={'class': 'form-control'}),
        }

    year = forms.ChoiceField(
        choices=[(str(year), str(year)) for year in range(1980, 2050)])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    year = forms.ChoiceField(
        choices=[(str(year), str(year)) for year in range(1980, 2050)])

    def __init__(self, *args, **kwargs):
        super(PrefectForm, self).__init__(*args, **kwargs)

        # Don't hide the field here - let the JavaScript handle it
        # Just set the required attribute based on form data
        if self.data:
            prefect_type = self.data.get('prefect_type')
            if prefect_type == 'Class Monitor':  # Match the exact choice value
                self.fields['class_level'].required = True
            else:
                self.fields['class_level'].required = False
        else:
            self.fields['class_level'].required = False
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

    def clean(self):
        cleaned_data = super().clean()
        prefect_type = cleaned_data.get('prefect_type')
        class_level = cleaned_data.get('class_level')
        student = cleaned_data.get('student')
        year = cleaned_data.get('year')

        # Validate that class_level is provided when prefect_type is 'Class Monitor'
        if prefect_type == 'Class Monitor' and not class_level:
            self.add_error(
                'class_level', 'Class level is required for Class Monitor.')

        # Clear class_level if prefect_type is not 'Class Monitor'
        if prefect_type != 'Class Monitor':
            cleaned_data['class_level'] = None

        # Check if a Prefect with the same student and year already exists
        if Prefect.objects.filter(student=student, year=year).exists():
            raise ValidationError("This student already has a prefect role assigned for the year {}.".format(year))

        return cleaned_data
