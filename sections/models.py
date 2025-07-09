from django.db import models


class Section(models.Model):
    section_name = models.CharField(max_length=255)
    section_code = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.section_name} ({self.section_code})"
