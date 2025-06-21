from django.db import models
from users.models import CustomUser

class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,null=True, limit_choices_to={'role': 'student'})
    guardian = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='wards', limit_choices_to={'role': 'guardian'})
    date_of_birth = models.DateField()
    admission_date = models.DateField(auto_now_add=True)
    health_issues = models.TextField(blank=True)
    class_level = models.CharField(max_length=50)
    address = models.TextField()

    # New fields for the student
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=200, blank=True)
    student_number = models.CharField(max_length=50, unique=True)
    telephone_number = models.CharField(max_length=15, blank=True)
    whatsapp_number = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    # In your models.py
    profile_photo = models.ImageField(upload_to='profiles/', blank=True, null=True)




    def __str__(self):
        return self.full_name
