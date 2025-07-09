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
        fields = ['teacher', 'leave_type',
                  'from_date', 'to_date', 'description']
        widgets = {
            'from_date': forms.DateInput(attrs={'type': 'date'}),
            'to_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(LeaveRequestForm, self).__init__(*args, **kwargs)
        # Make teacher field read-only
        self.fields['teacher'].widget.attrs['readonly'] = True
        # All teachers can be selected
        self.fields['teacher'].queryset = Teacher.objects.all()
        # All leave types can be selected
        self.fields['leave_type'].queryset = LeaveType.objects.all()


class LeaveAllocationForm(forms.ModelForm):
    class Meta:
        model = LeaveAllocation
        fields = ['teacher', 'casual_leave', 'sick_leave', 'year']
