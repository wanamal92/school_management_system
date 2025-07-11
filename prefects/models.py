from django.db import models
# Assuming you have the Student model in students app
from students.models import Student
from clases.models import Class


class Prefect(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="prefect")
    prefect_type = models.CharField(max_length=255, choices=[
        ('Senior Head Prefect', 'Senior Head Prefect'),
        ('Senior Deputy Head Prefect', 'Senior Deputy Head Prefect'),
        ('Prefect (Oriental Section)', 'Prefect (Oriental Section)'),
        ('Student Services Coordinator', 'Student Services Coordinator'),
        ('Junior Head Prefect', 'Junior Head Prefect'),
        ('Junior Deputy Head Prefect', 'Junior Deputy Head Prefect'),
        ('Prefect (Primary Section)', 'Prefect (Primary Section)'),
        ('Class Monitor', 'Class Monitor'),
    ])
    class_level = models.ForeignKey(
        Class, on_delete=models.SET_NULL, null=True, blank=True, related_name="class_level")
    assigned_date = models.DateField(auto_now_add=True)
    year = models.PositiveIntegerField()

    class Meta:
        unique_together = ('student', 'year')

    def __str__(self):
        return f"{self.student.full_name} - {self.prefect_type.name}"
