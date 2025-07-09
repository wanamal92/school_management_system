from django.db import models
from students.models import Student  # Assuming you have a Student model
from teachers.models import Teacher  # Assuming you have a Teacher model


class HealthRecord(models.Model):
    # Define choices for the type of record (Student or Teacher)
    TYPE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    ]

    # Type of record (Student or Teacher)
    record_type = models.CharField(max_length=7, choices=TYPE_CHOICES)

    # Dynamically link to either a student or teacher based on the record type
    student = models.OneToOneField(
        Student, on_delete=models.CASCADE, null=True, blank=True)
    teacher = models.OneToOneField(
        Teacher, on_delete=models.CASCADE, null=True, blank=True)

    # Health fields
    height_cm = models.FloatField()
    weight_kg = models.FloatField()
    eye_glasses = models.BooleanField(default=False)
    physical_challenge = models.BooleanField(default=False)
    major_diseases = models.BooleanField(default=False)
    regular_checkup_required = models.BooleanField(default=False)

    def __str__(self):
        return f"Health Record for {self.student if self.record_type == 'student' else self.teacher}"
