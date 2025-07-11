from django import forms
from .models import Class
from teachers.models import Teacher
from sections.models import Section


class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['class_name', 'class_code', 'section', 'class_in_charge']

    class_in_charge = forms.ModelChoiceField(
        queryset=Teacher.objects.all(), empty_label="Select Teacher", required=False)
    section = forms.ModelChoiceField(
        queryset=Section.objects.all(), empty_label="Select Section", required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_class_name(self):
        class_name = self.cleaned_data.get('class_name')
        # Ensure class name is provided
        if not class_name:
            raise forms.ValidationError("Class name is required.")
        if len(class_name) < 3:
            raise forms.ValidationError("Class name must be at least 3 characters long.")
        return class_name

    def clean_class_code(self):
        class_code = self.cleaned_data.get('class_code')
        # Ensure class code is provided
        if not class_code:
            raise forms.ValidationError("Class code is required.")
        # Ensure class code is unique
        if Class.objects.filter(class_code=class_code).exists():
            raise forms.ValidationError("This class code is already in use.")
        # Ensure the class code follows a specific format (e.g., alphanumeric and 5-10 characters)
        if not class_code.isalnum() or len(class_code) < 5 or len(class_code) > 10:
            raise forms.ValidationError("Class code must be alphanumeric and between 5 and 10 characters.")
        return class_code

    def clean_section(self):
        section = self.cleaned_data.get('section')
        # Ensure section is selected
        if not section:
            raise forms.ValidationError("Section is required.")
        return section

    def clean_class_in_charge(self):
        class_in_charge = self.cleaned_data.get('class_in_charge')
        # Ensure class_in_charge is selected
        if not class_in_charge:
            raise forms.ValidationError("Class in charge is required.")
        # You can also add a check to ensure that the teacher is not already assigned to another class
        if Class.objects.filter(class_in_charge=class_in_charge).exists():
            raise forms.ValidationError("This teacher is already assigned to another class.")
        return class_in_charge

    def clean(self):
        cleaned_data = super().clean()
        section = cleaned_data.get('section')
        class_in_charge = cleaned_data.get('class_in_charge')

        # Ensure that if a section is provided, there should be a class in charge
        if section and not class_in_charge:
            raise forms.ValidationError("If a section is selected, a class in charge must be provided.")
        
        return cleaned_data
