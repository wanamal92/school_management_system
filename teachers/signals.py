# teachers/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Teacher
from users.models import AuditLog
import secrets
import string

# Utility function to generate a random password


def generate_random_password():
    alphabet = string.ascii_letters + string.digits + string.punctuation
    # Generates a 12-character random password
    password = ''.join(secrets.choice(alphabet) for i in range(12))
    return password


@receiver(post_save, sender=Teacher)
def create_user_for_teacher(sender, instance, created, **kwargs):
    if created and not instance.user:  # Only create user if it's a new teacher and no user is linked
        # Generate the initial username using the first letter of first name and the first letter of last name
        base_username = instance.first_name.lower() + \
            instance.last_name[0].lower()
        print("==============================================")
        # Check if the username already exists in the database
        User = get_user_model()
        username = base_username

        # If the username exists, append the second letter of the last name and check again
        if User.objects.filter(username=username).exists():
            # Add the second letter of the last name
            username = base_username + instance.last_name[1].lower()

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
            full_name=instance.full_name,
            username=username,
            first_name=instance.first_name,
            last_name=instance.last_name,
            role='staff',  # Automatically set role to 'teacher'
            email=instance.email,  # Link email from teacher
            password=temp_password  # Set a temporary password
        )

        # Mark the user as needing a password change
        user.must_change_password = True
        if instance.profile_photo:
            user.profile_image = instance.profile_photo
        user.save()  # Save the user with must_change_password = True

        # Link the user to the teacher
        instance.user = user
        instance.save()  # Save the teacher with the new user

        # Create an audit log entry for user creation
        AuditLog.objects.create(
            # The user who performed the action (the created teacher)
            performed_by=instance.user,
            target_user=user,  # The user that was created
            action='create'
        )
