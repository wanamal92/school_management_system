from django import forms

from users.models import CustomUser
from .models import Guardian

from django.core.exceptions import ValidationError


class GuardianForm(forms.ModelForm):

    class Meta:
        model = Guardian
        fields = [
            'title', 'first_name', 'last_name', 'full_name', 'gender', 'phone',
            'mobile', 'email', 'address', 'profile_photo'
        ]

    

        widgets = {
            'birthdate': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 4, 'cols': 50}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    # Custom validation for 'first_name'
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        
        # Ensure first name is not empty and reasonable length
        if not first_name:
            raise ValidationError("First name cannot be empty.")
        if len(first_name) > 100:
            raise ValidationError("First name cannot be longer than 100 characters.")
        
        return first_name

    # Custom validation for 'last_name'
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        
        # Ensure last name is not empty and reasonable length
        if not last_name:
            raise ValidationError("Last name cannot be empty.")
        if len(last_name) > 100:
            raise ValidationError("Last name cannot be longer than 100 characters.")
        
        return last_name

    # Custom validation for 'full_name' to ensure it has the right format (optional)
    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        
        # If full name is provided, ensure it's not too long
        if full_name and len(full_name) > 200:
            raise ValidationError("Full name cannot be longer than 200 characters.")
        
        return full_name

    # Custom validation for 'phone' and 'mobile' to ensure they contain only digits
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        # Validate phone number length and characters
        if not phone.isdigit():
            raise ValidationError("Phone number must contain only digits.")
        if len(phone) < 10 or len(phone) > 15:
            raise ValidationError("Phone number must be between 10 and 15 digits.")
        
        return phone

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')

        # Validate mobile number length and characters
        if not mobile.isdigit():
            raise ValidationError("Mobile number must contain only digits.")
        if len(mobile) < 10 or len(mobile) > 15:
            raise ValidationError("Mobile number must be between 10 and 15 digits.")
        
        return mobile

    # Custom validation for 'email' to ensure it's valid
    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        # Only validate email if it's provided
        if email:
            if '@' not in email:
                raise ValidationError("Please enter a valid email address.")
        
        return email

    # Custom validation for 'profile_photo' to ensure it's an image and not too large
    def clean_profile_photo(self):
        profile_photo = self.cleaned_data.get('profile_photo')
        
        if profile_photo:
            # Ensure the file is an image
            if not profile_photo.name.lower().endswith(('jpg', 'jpeg', 'png')):
                raise ValidationError("Profile photo must be an image (jpg, jpeg, png).")

            # Optional: You can limit the file size to 5MB (for example)
            if profile_photo.size > 5 * 1024 * 1024:  # 5MB
                raise ValidationError("Profile photo size must be under 5MB.")
        
        return profile_photo

    # Custom validation for 'address' to ensure it's not too long
    def clean_address(self):
        address = self.cleaned_data.get('address')
        
        if len(address) > 1000:
            raise ValidationError("Address cannot be longer than 1000 characters.")
        
        return address
