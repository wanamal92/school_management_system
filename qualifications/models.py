# models.py
from django.db import models
from teachers.models import Teacher


class Qualification(models.Model):
    name = models.CharField(max_length=255, unique=True)
    short_code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name


class TeacherQualification(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    qualification = models.ForeignKey(Qualification, on_delete=models.CASCADE)
    institute = models.CharField(max_length=255)
    date_obtained = models.DateField()

    def __str__(self):
        return f'{self.teacher.name} - {self.qualification.name}'
