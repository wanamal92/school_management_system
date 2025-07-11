from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django.core.exceptions import ValidationError
import re


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['full_name', 'username', 'email', 'role', 'profile_image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    # Custom validation for 'email'
    def clean_email(self):
        email = self.cleaned_data.get('email')

        # Ensure the email is valid
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValidationError("Please enter a valid email address.")

        return email

    # Custom validation for 'role' to ensure it is one of the predefined choices
    def clean_role(self):
        role = self.cleaned_data.get('role')

        if role not in dict(CustomUser.ROLE_CHOICES):
            raise ValidationError(f"Invalid role selected. Choose from {', '.join(dict(CustomUser.ROLE_CHOICES).values())}")

        return role


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['full_name', 'username', 'email', 'role', 'profile_image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    # Custom validation for 'email' to ensure it's unique
    def clean_email(self):
        email = self.cleaned_data.get('email')

        # Ensure the email is unique, but allow the user to keep their existing email
        if CustomUser.objects.exclude(id=self.instance.id).filter(email=email).exists():
            raise ValidationError(f"The email '{email}' is already taken. Please choose a different one.")

        return email

    # Custom validation for 'role' to ensure it is valid
    def clean_role(self):
        role = self.cleaned_data.get('role')

        if role not in dict(CustomUser.ROLE_CHOICES):
            raise ValidationError(f"Invalid role selected. Choose from {', '.join(dict(CustomUser.ROLE_CHOICES).values())}")

        return role
