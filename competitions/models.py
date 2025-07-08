from django.db import models
from students.models import Student

# Competition model
class Competition(models.Model):
    COMPETITION_TYPES = [
        ('District', 'District'),
        ('All Island', 'All Island'),
    ]
    
    name = models.CharField(max_length=255)
    competition_type = models.CharField(max_length=10, choices=COMPETITION_TYPES)

    def __str__(self):
        return self.name

# CompetitionResult model
class CompetitionResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    year = models.PositiveIntegerField()
    result = models.CharField(max_length=15, choices=[
        ('First Place', 'First Place'),
        ('Second Place', 'Second Place'),
        ('Third Place', 'Third Place'),
        ('Fourth Place', 'Fourth Place'),
        ('Fifth Place', 'Fifth Place'),
    ])

    def __str__(self):
        return f"{self.student} - {self.competition} - {self.result} ({self.year})"
