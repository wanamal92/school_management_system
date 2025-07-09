from django.db import models
from teachers.models import Teacher
from sections.models import Section


class Class(models.Model):
    class_name = models.CharField(max_length=255)
    class_code = models.CharField(max_length=100, unique=True)
    section = models.ForeignKey(
        Section, on_delete=models.SET_NULL, null=True, blank=True)
    class_in_charge = models.OneToOneField(
        Teacher, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.class_name} - {self.section} ({self.class_code})"
