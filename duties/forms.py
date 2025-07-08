from django import forms
from .models import Duty, TeacherDuty
from teachers.models import Teacher

# Form for creating/updating Duty
class DutyForm(forms.ModelForm):
    class Meta:
        model = Duty
        fields = ['name']

# Form for creating/updating TeacherDuty
class TeacherDutyForm(forms.ModelForm):
    class Meta:
        model = TeacherDuty
        fields = ['teacher', 'duty', 'year']

    year = forms.ChoiceField(choices=[(str(year), str(year)) for year in range(1980, 2050)])
