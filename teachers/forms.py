# teachers/forms.py

from django import forms

from users.models import CustomUser
from .models import Teacher

class TeacherForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(role='staff'), 
        empty_label="Select Teacher User",
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Teacher
        fields = [
            'user', 'title', 'first_name', 'last_name','full_name', 'shortcode', 'gender', 'phone',
            'mobile', 'birthdate', 'nationality', 'emergency_contact', 'section', 'address', 'profile_photo'
        ]
        
        widgets = {
            'birthdate': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 4, 'cols': 50}),
        }
