from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('guardian', 'Guardian'),
        ('student', 'Student'),
    )
    full_name = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    profile_image = models.ImageField(upload_to='profiles/', default='default.png')
    must_change_password = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name
    
    

class AuditLog(models.Model):
    ACTION_CHOICES = (
        ('create', 'Created'),
        ('delete', 'Deleted'),
        ('deactivate', 'Deactivated'),
        ('reactivate', 'Reactivated'),
    )

    performed_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='performed_logs')
    target_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='affected_logs')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.performed_by} {self.get_action_display()} {self.target_user} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
