from django import forms

from users.models import CustomUser
from .models import Guardian

class GuardianForm(forms.ModelForm):
    
    class Meta:
        model = Guardian
        fields = [
            'title', 'first_name', 'last_name','full_name', 'gender', 'phone',
            'mobile','email', 'address', 'profile_photo'
        ]
        
        widgets = {
            'birthdate': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 4, 'cols': 50}),
        }
