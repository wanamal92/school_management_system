from django import forms
from .models import LeaveRequest, LeaveAllocation, LeaveType
from teachers.models import Teacher


class LeaveTypeForm(forms.ModelForm):
    class Meta:
        model = LeaveType
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter leave type name (e.g. Casual Leave, Sick Leave)'}),
        }



class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['teacher', 'leave_type', 'from_date', 'to_date', 'description']
        widgets = {
            'from_date': forms.DateInput(attrs={'type': 'date'}),
            'to_date': forms.DateInput(attrs={'type': 'date'}),
        }

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
