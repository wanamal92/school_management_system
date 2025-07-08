from django import forms
from .models import Competition, CompetitionResult
from students.models import Student

# Form for creating/updating Competition
class CompetitionForm(forms.ModelForm):
    class Meta:
        model = Competition
        fields = ['name', 'competition_type']

# Form for creating/updating CompetitionResult
class CompetitionResultForm(forms.ModelForm):
    class Meta:
        model = CompetitionResult
        fields = ['student', 'competition', 'year', 'result']
    
    year = forms.ChoiceField(choices=[(str(year), str(year)) for year in range(1980, 2050)])
