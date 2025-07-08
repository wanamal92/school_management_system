
from django.db import models
from users.models import CustomUser
from guardians.models import Guardian
from clases.models import Class
"""
    Model to store student information, including personal details
"""

class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,null=True, limit_choices_to={'role': 'student'})
    guardian = models.ForeignKey(Guardian, on_delete=models.SET_NULL, null=True, blank=True, related_name='wards')
    date_of_birth = models.DateField()
    admission_date = models.DateField(auto_now_add=True)
    class_level = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, blank=True, related_name='class_l')
    address = models.TextField()

    # New fields for the student
    title = models.CharField(max_length=10, choices=[('Rev', 'Rev'),('Mr', 'Mr')])
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=200, blank=True)
    student_number = models.CharField(max_length=50, unique=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    telephone_number = models.CharField(max_length=15, blank=True)
    whatsapp_number = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    # In your models.py
    profile_photo = models.ImageField(upload_to='profiles/', blank=True, null=True)




    def __str__(self):
        return self.full_name
