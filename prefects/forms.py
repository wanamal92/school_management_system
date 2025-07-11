from django import forms
from .models import Prefect
from students.models import Student
from clases.models import Class


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

    def clean(self):
        cleaned_data = super().clean()
        prefect_type = cleaned_data.get('prefect_type')
        class_level = cleaned_data.get('class_level')

        # Validate that class_level is provided when prefect_type is 'Class Monitor'
        if prefect_type == 'Class Monitor' and not class_level:
            self.add_error(
                'class_level', 'Class level is required for Class Monitor.')

        # Clear class_level if prefect_type is not 'Class Monitor'
        if prefect_type != 'Class Monitor':
            cleaned_data['class_level'] = None

        return cleaned_data
