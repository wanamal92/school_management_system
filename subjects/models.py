from django.db import models
from teachers.models import Teacher
from clases.models import Class  # Assuming you already have the Class model

class Subject(models.Model):
    subject_name = models.CharField(max_length=255)
    subject_code = models.CharField(max_length=100, unique=True)
    class_assigned = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.subject_name} ({self.subject_code})"

class TeacherSubject(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.subject.subject_name} - {self.teacher.full_name}"
