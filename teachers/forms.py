# teachers/forms.py

from django import forms

from users.models import CustomUser
from .models import Teacher
from sections.models import Section
from django.core.exceptions import ValidationError
import re

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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    # Custom validation for 'shortcode' to ensure it's unique
    def clean_shortcode(self):
        shortcode = self.cleaned_data.get('shortcode')

        # Ensure the shortcode is unique
        if Teacher.objects.filter(shortcode=shortcode).exists():
            raise ValidationError(f"The shortcode '{shortcode}' is already taken. Please choose a different one.")

        return shortcode

    # Custom validation for 'birthdate' to ensure the date is not in the future
    def clean_birthdate(self):
        birthdate = self.cleaned_data.get('birthdate')

        if birthdate > date.today():
            raise ValidationError("Birthdate cannot be in the future.")

        return birthdate

    # Custom validation for 'phone', 'mobile', and 'emergency_contact' to ensure only numeric values
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if phone and not phone.isdigit():
            raise ValidationError("Phone number should only contain digits.")

        return phone

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')

        if mobile and not mobile.isdigit():
            raise ValidationError("Mobile number should only contain digits.")

        return mobile

    def clean_emergency_contact(self):
        emergency_contact = self.cleaned_data.get('emergency_contact')

        if emergency_contact and not emergency_contact.isdigit():
            raise ValidationError("Emergency contact number should only contain digits.")

        return emergency_contact

    # Automatically generate 'full_name' based on 'first_name' and 'last_name' if not provided
    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')

        if not full_name:
            first_name = self.cleaned_data.get('first_name')
            last_name = self.cleaned_data.get('last_name')
            full_name = f"{first_name} {last_name}"

        return full_name
