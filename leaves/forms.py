from django import forms
from .models import LeaveRequest, LeaveAllocation, LeaveType
from teachers.models import Teacher
from django.core.exceptions import ValidationError


class LeaveTypeForm(forms.ModelForm):
    class Meta:
        model = LeaveType
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter leave type name (e.g. Casual Leave, Sick Leave)'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    # Custom validation for 'name' field
    def clean_name(self):
        name = self.cleaned_data.get('name')

        # Ensure name is not empty
        if not name:
            raise ValidationError("Leave type name cannot be empty.")

        # Ensure name is not too long (max length is 100 characters in model)
        if len(name) > 100:
            raise ValidationError("Leave type name cannot be longer than 100 characters.")

        # Ensure the name is unique (no other LeaveType exists with this name)
        if LeaveType.objects.exclude(id=self.instance.id).filter(name=name).exists():
            raise ValidationError(f"The leave type '{name}' already exists. Please choose a different name.")

        return name



class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['teacher', 'leave_type', 'from_date', 'to_date', 'description']
        widgets = {
            'from_date': forms.DateInput(attrs={'type': 'date'}),
            'to_date': forms.DateInput(attrs={'type': 'date'}),
        }




    # Custom validation for 'from_date' and 'to_date' to ensure correct range
    def clean(self):
        cleaned_data = super().clean()
        from_date = cleaned_data.get('from_date')
        to_date = cleaned_data.get('to_date')

        # Ensure from_date is not after to_date
        if from_date and to_date:
            if from_date > to_date:
                raise ValidationError("From date cannot be after to date.")

        return cleaned_data

    # Custom validation for 'description' field (optional)
    def clean_description(self):
        description = self.cleaned_data.get('description')

        # Ensure description is not too long (optional limit)
        if len(description) < 10:
            raise ValidationError("Description must be at least 10 characters long.")
        if len(description) > 1000:
            raise ValidationError("Description cannot be longer than 1000 characters.")
        
        return description

    def save(self, *args, **kwargs):
        # First, we check if the leave request can be approved
        leave_request = super().save(commit=False)

        if leave_request.status == 'Approved':
            # Check if teacher has enough leave balance before approving
            teacher_leave_allocation = leave_request.teacher.leaveallocation
            if leave_request.leave_type.name == "Casual Leave":
                if teacher_leave_allocation.casual_leave < leave_request.duration:
                    raise ValidationError("Not enough Casual Leave balance available.")

            elif leave_request.leave_type.name == "Sick Leave":
                if teacher_leave_allocation.sick_leave < leave_request.duration:
                    raise ValidationError("Not enough Sick Leave balance available.")
        
        # Save the valid leave request and deduct leave from the teacher's allocation
        leave_request.save()
        
        # Deduct the leave from the teacher's leave allocation
        if leave_request.status == 'Approved':
            if leave_request.leave_type.name == "Casual Leave":
                teacher_leave_allocation.casual_leave -= leave_request.duration
            elif leave_request.leave_type.name == "Sick Leave":
                teacher_leave_allocation.sick_leave -= leave_request.duration
            teacher_leave_allocation.save()

        return leave_request
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'



    def __init__(self, *args, **kwargs):
        # We need to get the logged-in user from the kwargs
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            # Fetch the teacher instance corresponding to the logged-in user
            teacher = Teacher.objects.get(user=user)
            # Set the teacher field to the logged-in teacher and make it read-only
            self.fields['teacher'].initial = teacher
            self.fields['teacher'].queryset = Teacher.objects.filter(user=user)  # Limit to the logged-in teacher
            self.fields['teacher'].widget.attrs['readonly'] = 'readonly'  # Make the teacher field readonly


class LeaveAllocationForm(forms.ModelForm):
    class Meta:
        model = LeaveAllocation
        fields = ['teacher', 'casual_leave', 'sick_leave', 'year']

    # Custom validation for 'teacher'
    def clean_teacher(self):
        teacher = self.cleaned_data.get('teacher')
        if not Teacher.objects.filter(id=teacher.id).exists():
            raise ValidationError("The selected teacher does not exist.")
        return teacher

    # Custom validation for 'year' to ensure it is within the valid range
    def clean_year(self):
        year = self.cleaned_data.get('year')
        if year < 2025 or year > 2050:
            raise ValidationError("Year must be between 2025 and 2050.")
        return year

    # Custom validation for 'casual_leave' and 'sick_leave'
    def clean(self):
        cleaned_data = super().clean()
        casual_leave = cleaned_data.get('casual_leave')
        sick_leave = cleaned_data.get('sick_leave')

        # Ensure casual_leave and sick_leave are positive numbers
        if casual_leave < 0:
            raise ValidationError("Casual leave must be a positive number.")
        if sick_leave < 0:
            raise ValidationError("Sick leave must be a positive number.")

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
