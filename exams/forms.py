# exams/forms.py
from django import forms
from .models import ExamSession
from .models import Exam
from django.core.exceptions import ValidationError
from subjects.models import Subject
from teachers.models import Teacher
from .models import ExamAttendee
from students.models import Student
import re
import os


from datetime import datetime


class ExamSessionForm(forms.ModelForm):
    class Meta:
        model = ExamSession
        fields = ['exam_session_name', 'exam_session_code', 'start_date',
                  'end_date', 'exam_type', 'academic_year', 'class_assigned']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'



    # Custom validation for 'exam_session_name'
    def clean_exam_session_name(self):
        exam_session_name = self.cleaned_data.get('exam_session_name')
        if not exam_session_name:
            raise ValidationError("Exam session name cannot be empty.")
        return exam_session_name

    # Custom validation for 'exam_session_code' to ensure it's unique
    def clean_exam_session_code(self):
        exam_session_code = self.cleaned_data.get('exam_session_code')
        if ExamSession.objects.exclude(id=self.instance.id).filter(exam_session_code=exam_session_code).exists():
            raise ValidationError(
                f"Exam session code '{exam_session_code}' already exists.")
        return exam_session_code

    # Custom validation for 'start_date' and 'end_date'
    def clean_end_date(self):
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')

        if end_date < start_date:
            raise ValidationError(
                "End date cannot be earlier than start date.")
        return end_date

    # Custom validation for 'exam_type' to ensure it's selected correctly
    def clean_exam_type(self):
        exam_type = self.cleaned_data.get('exam_type')
        valid_exam_types = dict(ExamSession.EXAM_TYPE_CHOICES).keys()

        if exam_type not in valid_exam_types:
            raise ValidationError("Please select a valid exam type.")
        return exam_type

    def clean_academic_year(self):
        academic_year = self.cleaned_data.get('academic_year')
        academic_year = int(academic_year)

        # Ensure year is within the valid range
        if academic_year < 1980 or academic_year > 2050:
            raise ValidationError("Year must be between 1980 and 2050.")

        return academic_year

    # Custom validation for 'class_assigned' to ensure it's assigned
    def clean_class_assigned(self):
        class_assigned = self.cleaned_data.get('class_assigned')

        if not class_assigned:
            raise ValidationError("Please assign a class to the exam session.")

        return class_assigned


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['exam_session', 'exam_name',
                  'start_time', 'end_time', 'responsible_teacher']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    # Custom validation for 'exam_name'
    def clean_exam_name(self):
        exam_name = self.cleaned_data.get('exam_name')

        # Ensure the exam_name is a valid subject
        if not exam_name:
            raise ValidationError("Please select a valid exam name (subject).")

        return exam_name

    # Custom validation for 'start_time' and 'end_time'
    def clean_end_time(self):
        start_time = self.cleaned_data.get('start_time')
        end_time = self.cleaned_data.get('end_time')

        if end_time <= start_time:
            raise ValidationError(
                "End time cannot be earlier than or the same as start time.")

        return end_time

    # Custom validation for 'responsible_teacher'
    def clean_responsible_teacher(self):
        responsible_teacher = self.cleaned_data.get('responsible_teacher')

        # Ensure the teacher exists and is assigned correctly
        if not Teacher.objects.filter(id=responsible_teacher.id).exists():
            raise ValidationError("The selected teacher does not exist.")

        return responsible_teacher

    # Override the save method to auto-generate the subject code if it's not provided
    def save(self, *args, **kwargs):
        instance = super().save(commit=False)

        # Auto-generate the subject code based on the exam name
        if not instance.subject_code:
            instance.subject_code = instance.exam_name.subject_code

        instance.save()  # Save the exam instance
        return instance


class ExamAttendeeForm(forms.ModelForm):
    class Meta:
        model = ExamAttendee
        fields = ['student', 'exam', 'status', 'exam_marks']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

        # Custom validation for 'student' field
    def clean_student(self):
        student = self.cleaned_data.get('student')

        # Ensure the student exists
        if not Student.objects.filter(id=student.id).exists():
            raise ValidationError("The selected student does not exist.")
        return student

    # Custom validation for 'exam' field
    def clean_exam(self):
        exam = self.cleaned_data.get('exam')

        # Ensure the exam exists
        if not Exam.objects.filter(id=exam.id).exists():
            raise ValidationError("The selected exam does not exist.")
        return exam

    # Custom validation for 'status' field
    def clean_status(self):
        status = self.cleaned_data.get('status')

        # Ensure the status is either 'present' or 'absent'
        if status not in dict(ExamAttendee.STATUS_CHOICES):
            raise ValidationError(
                "Invalid status. Please select 'present' or 'absent'.")
        return status

    # Custom validation for 'exam_marks'
    def clean_exam_marks(self):
        exam_marks = self.cleaned_data.get('exam_marks')

        # If marks are provided, ensure they are valid
        if exam_marks is not None:
            if exam_marks < 0 or exam_marks > 100:
                raise ValidationError("Exam marks must be between 0 and 100.")
        return exam_marks

    # Overriding the save method to automatically assign a grade based on exam_marks
    def save(self, *args, **kwargs):
        instance = super().save(commit=False)

        # Automatically assign grade based on marks if marks are provided
        if instance.exam_marks is not None:
            if instance.exam_marks >= 75:
                instance.grade = 'A'
            elif instance.exam_marks >= 65:
                instance.grade = 'B'
            elif instance.exam_marks >= 50:
                instance.grade = 'C'
            elif instance.exam_marks >= 35:
                instance.grade = 'S'
            else:
                instance.grade = 'W'

        instance.save()  # Save the instance after assigning the grade
        return instance


class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField()

    def clean_excel_file(self):
        excel_file = self.cleaned_data.get('excel_file')

        # Get the file extension
        file_extension = os.path.splitext(excel_file.name)[1].lower()

        # Allowed file extensions for Excel files
        allowed_extensions = ['.xls', '.xlsx']

        # Check if the file extension is valid
        if file_extension not in allowed_extensions:
            raise ValidationError(
                "Please upload a valid Excel file (.xls or .xlsx).")

        # You can also check for file content type (optional)
        # if 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' not in excel_file.content_type:
        #     raise ValidationError("Please upload a valid Excel file (.xls or .xlsx).")

        return excel_file
