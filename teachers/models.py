# teachers/models.py
from django.db import models
from users.models import CustomUser

class Teacher(models.Model):
    # Linking to User model with a one-to-one relationship
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,null=True, limit_choices_to={'role': 'staff'})
    
    # Teacher's personal details
    title = models.CharField(max_length=10, choices=[('Mr', 'Mr'), ('Mrs', 'Mrs'), ('Ms', 'Ms'), ('Dr', 'Dr'), ('Prof', 'Prof')])
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=200, blank=True)
    shortcode = models.CharField(max_length=50, unique=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    phone = models.CharField(max_length=15)
    mobile = models.CharField(max_length=15)
    email = models.EmailField(blank=True)

    # Personal Information
    birthdate = models.DateField()
    nationality = models.CharField(max_length=100)
    emergency_contact = models.CharField(max_length=15)
    section = models.CharField(max_length=50, choices=[('Primary Section', 'Primary Section'), ('Oriental Section', 'Oriental Section'), ('Primary and Oriental Section', 'Primary and Oriental Section')])
    address = models.TextField()

    # Profile photo field
    profile_photo = models.ImageField(upload_to='teacher_photos/', blank=True, null=True)

    def __str__(self):
        return self.full_name
