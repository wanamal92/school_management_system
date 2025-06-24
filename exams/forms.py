# exams/forms.py
from django import forms
from .models import ExamSession
from .models import Exam
from subjects.models import Subject
from teachers.models import Teacher
from .models import ExamAttendee
from students.models import Student

class ExamSessionForm(forms.ModelForm):
    class Meta:
        model = ExamSession
        fields = ['exam_session_name', 'exam_session_code', 'start_date', 'end_date', 'exam_type', 'academic_year', 'class_assigned']

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['exam_session', 'exam_name', 'start_time', 'end_time', 'responsible_teacher']

class ExamAttendeeForm(forms.ModelForm):
    class Meta:
        model = ExamAttendee
        fields = ['student','exam', 'status', 'exam_marks']