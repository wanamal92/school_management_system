from django import forms
from .models import Subject
from teachers.models import Teacher
from .models import Subject,TeacherSubject
from django.forms import inlineformset_factory

class SubjectForm(forms.ModelForm):


    class Meta:
        model = Subject
        fields = ['subject_name', 'subject_code', 'class_assigned']


class TeacherSubjectForm(forms.ModelForm):
    class Meta:
        model = TeacherSubject
        fields = ['teacher']  # subject is auto-set in the view

# Inline formset
TeacherSubjectFormSet = inlineformset_factory(
    Subject, TeacherSubject, form=TeacherSubjectForm,
    extra=1, can_delete=True
)