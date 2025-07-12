from django import forms
from django.core.exceptions import ValidationError
from .models import Student, Class, Guardian
import re
from datetime import date

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'title', 'first_name', 'last_name', 'full_name', 'student_number', 'gender', 'telephone_number',
            'whatsapp_number', 'email', 'date_of_birth', 'class_level', 'guardian', 'address', 'profile_photo'
        ]

        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            
        }
        
    class_level = forms.ModelChoiceField(
        queryset=Class.objects.all(), empty_label="Select Class")
    
    guardian = forms.ModelChoiceField(
        queryset=Guardian.objects.all().order_by("full_name"), empty_label="Select Guardian")

    # Custom validation for 'student_number' to ensure it's unique
    def clean_student_number(self):
        student_number = self.cleaned_data.get('student_number')
        
        if Student.objects.exclude(id=self.instance.id).filter(student_number=student_number).exists():
            raise ValidationError(f"Student number '{student_number}' is already taken. Please choose a different one.")
        
        return student_number

    # Custom validation for 'date_of_birth' to ensure the date is not in the future
    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        
        if date_of_birth > date.today():
            raise ValidationError("Date of birth cannot be in the future.")
        
        return date_of_birth

    # Custom validation for 'telephone_number' and 'whatsapp_number' (should only contain digits)
    def clean_telephone_number(self):
        telephone_number = self.cleaned_data.get('telephone_number')
        
        if telephone_number and not telephone_number.isdigit():
            raise ValidationError("Telephone number should only contain digits.")
        
        return telephone_number

    def clean_whatsapp_number(self):
        whatsapp_number = self.cleaned_data.get('whatsapp_number')
        
        if whatsapp_number and not whatsapp_number.isdigit():
            raise ValidationError("WhatsApp number should only contain digits.")
        
        return whatsapp_number

    # Custom validation for 'email' to ensure it is in the correct format (optional)
    def clean_email(self):
        email = self.cleaned_data.get('email')

        if email:
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                raise ValidationError("Please enter a valid email address.")
        
        return email

    # Automatically generate 'full_name' based on 'first_name' and 'last_name' if not provided
    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        
        if not full_name:
            first_name = self.cleaned_data.get('first_name')
            last_name = self.cleaned_data.get('last_name')
            full_name = f"{first_name} {last_name}"
        
        return full_name


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
