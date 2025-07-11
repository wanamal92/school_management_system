from django import forms
from .models import Subject
from teachers.models import Teacher
from .models import Subject, TeacherSubject
from django.forms import inlineformset_factory
from django.core.exceptions import ValidationError


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['subject_name', 'subject_code', 'class_assigned']

    # Custom validation for 'subject_name'
    def clean_subject_name(self):
        subject_name = self.cleaned_data.get('subject_name')
        
        if not subject_name:
            raise ValidationError("Subject name cannot be empty.")
        
        return subject_name

    # Custom validation for 'subject_code' to ensure it's unique
    def clean_subject_code(self):
        subject_code = self.cleaned_data.get('subject_code')
        
        # Ensure the subject_code is unique
        if Subject.objects.filter(subject_code=subject_code).exists():
            raise ValidationError(f"The subject code '{subject_code}' is already taken. Please choose a different one.")
        
        return subject_code

    # Custom validation for 'class_assigned' to ensure it's not empty
    def clean_class_assigned(self):
        class_assigned = self.cleaned_data.get('class_assigned')
        
        if not class_assigned:
            raise ValidationError("Please assign a class for the subject.")
        
        return class_assigned

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply Bootstrap form-control to all fields for styling
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'



class TeacherSubjectForm(forms.ModelForm):
    class Meta:
        model = TeacherSubject
        fields = ['teacher']  # subject is auto-set in the view
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


# Inline formset
TeacherSubjectFormSet = inlineformset_factory(
    Subject, TeacherSubject, form=TeacherSubjectForm,
    extra=1, can_delete=True
)
