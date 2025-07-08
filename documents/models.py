
from django.db import models
from teachers.models import Teacher
from students.models import Student


class Document(models.Model):
    DOCUMENT_TYPES = [
        ('NIC', 'NIC'),
        ('Passport', 'Passport'),
        ('Birth Certificate', 'Birth Certificate'),
        ('Samanera Certificate', 'Samanera Certificate'),
        ('Upasampada Certificate', 'Upasampada Certificate'),
        ('School Leaving Certificate', 'School Leaving Certificate'),
        ('Competition Certificate', 'Competition Certificate'),
    ]
    USER_TYPES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    ]

    # Type of record (Student or Teacher)
    user_type = models.CharField(max_length=7, choices=USER_TYPES)
    
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, blank=True, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True, null=True)
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPES)
    document_file = models.FileField(upload_to='documents/')  # Store the file
    expire_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.document_type} - {self.teacher if self.teacher else self.student}"

    class Meta:
        verbose_name_plural = 'Documents'
