# exams/models.py
from django.db import models
from clases.models import Class  # Assuming you have a Class model
from subjects.models import Subject  # Assuming you have a Subject model
from teachers.models import Teacher
from students.models import Student


class ExamSession(models.Model):
    EXAM_TYPE_CHOICES = [
        ('first_term', 'First Term'),
        ('mid_term', 'Mid Term'),
        ('final_term', 'Final Term')
    ]

    exam_session_name = models.CharField(max_length=255)
    exam_session_code = models.CharField(max_length=100, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    exam_type = models.CharField(max_length=50, choices=EXAM_TYPE_CHOICES)
    academic_year = models.CharField(max_length=20)
    class_assigned = models.ForeignKey(Class, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.exam_session_name} ({self.exam_session_code})"


class Exam(models.Model):
    exam_session = models.ForeignKey(ExamSession, on_delete=models.CASCADE)
    exam_name = models.ForeignKey(Subject, on_delete=models.CASCADE)
    subject_code = models.CharField(max_length=20, blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    responsible_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.subject_code:
            # Automatically generate the subject code
            self.subject_code = self.exam_name.subject_code
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.exam_name} ({self.subject_code})"


class ExamAttendee(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent')
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='absent')
    exam_marks = models.FloatField(null=True, blank=True)
    grade = models.CharField(max_length=2, null=True, blank=True)

    class Meta:
        unique_together = ('student', 'exam')

    def save(self, *args, **kwargs):
        if self.exam_marks is not None:
            if self.exam_marks >= 75:
                self.grade = 'A'
            elif self.exam_marks >= 65:
                self.grade = 'B'
            elif self.exam_marks >= 50:
                self.grade = 'C'
            elif self.exam_marks >= 35:
                self.grade = 'S'
            else:
                self.grade = 'W'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.full_name} - {self.exam.exam_name}"
