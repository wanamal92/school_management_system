# forms.py
from django import forms
from .models import HealthRecord
from students.models import Student
from teachers.models import Teacher
from django.core.exceptions import ValidationError


class HealthRecordForm(forms.ModelForm):
    class Meta:
        model = HealthRecord
        fields = [
            'record_type', 'student', 'teacher', 'height_cm', 'weight_kg',
            'eye_glasses', 'physical_challenge', 'major_diseases', 'regular_checkup_required'
        ]
        widgets = {
            'record_type': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_record_type'
            }),
            'student': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_student'
            }),
            'teacher': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_teacher'
            }),
            'height_cm': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'placeholder': 'Height in cm'
            }),
            'weight_kg': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'placeholder': 'Weight in kg'
            }),
            'eye_glasses': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'physical_challenge': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'major_diseases': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'regular_checkup_required': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Make both fields optional initially since JS will handle the logic
        self.fields['student'].required = False
        self.fields['teacher'].required = False

    def clean(self):
        cleaned_data = super().clean()
        record_type = cleaned_data.get('record_type')
        student = cleaned_data.get('student')
        teacher = cleaned_data.get('teacher')

        # Validate based on record_type
        if record_type == 'student':
            if not student:
                raise forms.ValidationError("Please select a student.")
            # Clear teacher field if student is selected
            cleaned_data['teacher'] = None
        elif record_type == 'teacher':
            if not teacher:
                raise forms.ValidationError("Please select a teacher.")
            # Clear student field if teacher is selected
            cleaned_data['student'] = None
        else:
            raise forms.ValidationError("Please select a record type.")

        # Validate height and weight
        height = cleaned_data.get('height_cm')
        weight = cleaned_data.get('weight_kg')

        if height <= 0:
            raise ValidationError("Height must be a positive number.")
        if weight <= 0:
            raise ValidationError("Weight must be a positive number.")

        return cleaned_data


# # forms.py
# from django import forms
# from .models import HealthRecord
# from students.models import Student
# from teachers.models import Teacher

# class HealthRecordForm(forms.ModelForm):
#     class Meta:
#         model = HealthRecord
#         fields = [
#             'record_type', 'student', 'teacher', 'height_cm', 'weight_kg',
#             'eye_glasses', 'physical_challenge', 'major_diseases', 'regular_checkup_required'
#         ]
#         widgets = {
#             'record_type': forms.Select(attrs={
#                 'class': 'form-control record-type-selector',
#                 'onchange': 'this.form.submit()'  # This will trigger form submission on change
#             }),
#             'student': forms.Select(attrs={
#                 'class': 'form-control student-field'
#             }),
#             'teacher': forms.Select(attrs={
#                 'class': 'form-control teacher-field'
#             }),
#             'height_cm': forms.NumberInput(attrs={
#                 'class': 'form-control',
#                 'step': '0.1',
#                 'placeholder': 'Height in cm'
#             }),
#             'weight_kg': forms.NumberInput(attrs={
#                 'class': 'form-control',
#                 'step': '0.1',
#                 'placeholder': 'Weight in kg'
#             }),
#             'eye_glasses': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
#             'physical_challenge': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
#             'major_diseases': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
#             'regular_checkup_required': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
#         }

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         # Get the record_type from POST data or instance
#         record_type = None
#         if self.data:
#             record_type = self.data.get('record_type')
#         elif self.instance.pk:
#             record_type = self.instance.record_type

#         # Show/hide fields based on record_type
#         if record_type == 'student':
#             self.fields['teacher'].widget = forms.HiddenInput()
#             self.fields['teacher'].required = False
#             self.fields['student'].required = True
#         elif record_type == 'teacher':
#             self.fields['student'].widget = forms.HiddenInput()
#             self.fields['student'].required = False
#             self.fields['teacher'].required = True
#         else:
#             # If no record_type selected, hide both fields initially
#             self.fields['student'].widget = forms.HiddenInput()
#             self.fields['teacher'].widget = forms.HiddenInput()
#             self.fields['student'].required = False
#             self.fields['teacher'].required = False

#     def clean(self):
#         cleaned_data = super().clean()
#         record_type = cleaned_data.get('record_type')
#         student = cleaned_data.get('student')
#         teacher = cleaned_data.get('teacher')

#         # Ensure only one field is filled based on record_type
#         if record_type == 'student':
#             if not student:
#                 raise forms.ValidationError("Please select a student.")
#             cleaned_data['teacher'] = None
#         elif record_type == 'teacher':
#             if not teacher:
#                 raise forms.ValidationError("Please select a teacher.")
#             cleaned_data['student'] = None
#         else:
#             raise forms.ValidationError("Please select a record type.")

#         return cleaned_data
