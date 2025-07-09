from django.db import models
from users.models import CustomUser


class Guardian(models.Model):
    # Linking to User model with a one-to-one relationship
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, null=True, limit_choices_to={'role': 'guardian'})

    # Guardian's personal details
    title = models.CharField(max_length=10, choices=[(
        'Rev', 'Rev'), ('Mr', 'Mr'), ('Mrs', 'Mrs'), ('Ms', 'Ms')])
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=200, blank=True)
    gender = models.CharField(max_length=10, choices=[
                              ('Male', 'Male'), ('Female', 'Female')])
    phone = models.CharField(max_length=15)
    mobile = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    address = models.TextField()
    profile_photo = models.ImageField(
        upload_to='guardian_photos/', blank=True, null=True)

    def __str__(self):
        return self.full_name
