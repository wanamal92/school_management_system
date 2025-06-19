# students/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Student  
from users.models import AuditLog
import secrets
import string

# Utility function to generate a random password
def generate_random_password():
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for i in range(12))  # Generates a 12-character random password
    return password

@receiver(post_save, sender=Student)
def create_user_for_student(sender, instance, created, **kwargs):
    if created and not instance.user:  # Only create user if it's a new student and no user is linked
        # Generate the initial username using the first letter of first name and the first letter of last name
        base_username = instance.first_name.lower() + instance.last_name[0].lower()

        # Check if the username already exists in the database
        User = get_user_model()
        username = base_username

        # If the username exists, append the second letter of the last name and check again
        if User.objects.filter(username=username).exists():
            username = base_username + instance.last_name[1].lower()  # Add the second letter of the last name

            # If still exists, check and append a counter (if needed)
            counter = 2
            while User.objects.filter(username=username).exists():
                username = username + instance.last_name[counter].lower()
                print(username)
                counter += 1

        # Generate a random temporary password
        temp_password = "TempPass123"

        # Create the CustomUser with the unique username
        user = User.objects.create_user(
            username=username,
            first_name=instance.first_name,
            last_name=instance.last_name,
            role='student',  # Automatically set role to 'student'
            email=instance.email,  # Link email from student
            password=temp_password  # Set a temporary password
        )

        # Mark the user as needing a password change
        user.must_change_password = True
        user.save()  # Save the user with must_change_password = True

        # Link the user to the student
        instance.user = user
        instance.save()  # Save the student with the new user

        # Create an audit log entry for user creation
        AuditLog.objects.create(
            performed_by=instance.user,  # The user who performed the action (the created student)
            target_user=user,  # The user that was created
            action='create'
        )
