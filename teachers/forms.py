# teachers/forms.py

from django import forms

from users.models import CustomUser
from .models import Teacher
from sections.models import Section


class TeacherForm(forms.ModelForm):

    class Meta:
        model = Teacher
        fields = [
            'title', 'first_name', 'last_name', 'full_name', 'shortcode', 'gender', 'phone',
            'mobile', 'email', 'birthdate', 'nationality', 'emergency_contact', 'section', 'address', 'profile_photo'
        ]
        section = forms.ModelChoiceField(
            queryset=Section.objects.all(), empty_label="Select Section")

        widgets = {
            'birthdate': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 4, 'cols': 50}),
        }
