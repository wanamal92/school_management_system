from django.db import models
from teachers.models import Teacher

# Duty model to store duty names


class Duty(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# TeacherDuty model to associate a teacher with a specific duty


class TeacherDuty(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    duty = models.ForeignKey(Duty, on_delete=models.CASCADE)
    year = models.PositiveIntegerField()

    class Meta:
        # Ensures each teacher can only have a duty once
        unique_together = ('teacher', 'duty', 'year')

    def __str__(self):
        return f"{self.teacher} - {self.duty} ({self.year})"
