from django.db import models
from teachers.models import Teacher
from django.db.models import F
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.utils import timezone


class LeaveType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class LeaveAllocation(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    casual_leave = models.IntegerField(
        default=14)  # 14 days casual leave annually
    sick_leave = models.IntegerField(default=7)  # 7 days sick leave annually
    year = models.PositiveIntegerField(null=False, blank=False)

    class Meta:
        unique_together = ('teacher', 'year')

    def __str__(self):
        return f"Leave Allocation for {self.teacher.full_name}"




class LeaveRequest(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    leave_type = models.ForeignKey(
        LeaveType, on_delete=models.SET_NULL, null=True)
    from_date = models.DateField()
    to_date = models.DateField()
    duration = models.IntegerField(blank=True, null=True)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), (
        'Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending')

    
    def save(self, *args, **kwargs):
        # Automatically calculate duration based on from_date and to_date
        if self.from_date and self.to_date:
            self.duration = (self.to_date - self.from_date).days + 1

        # Fetch the teacher's leave allocation for the current year
        year = timezone.now().year  # Get the current year
        try:
            leave_allocation = LeaveAllocation.objects.get(teacher=self.teacher, year=year)
        except LeaveAllocation.DoesNotExist:
            raise ValidationError(f"{self.teacher.full_name} does not have a leave allocation for the year {year}.")
        
        # Check if the teacher has enough leave days for the requested leave type
        if self.leave_type.name == "Casual Leave":
            if leave_allocation.casual_leave < self.duration:
                raise ValidationError(f"{self.teacher.full_name} does not have enough Casual Leave days remaining.")
            leave_allocation.casual_leave -= self.duration
        elif self.leave_type.name == "Sick Leave":
            if leave_allocation.sick_leave < self.duration:
                raise ValidationError(f"{self.teacher.full_name} does not have enough Sick Leave days remaining.")
            leave_allocation.sick_leave -= self.duration
        else:
            raise ValidationError("Unknown leave type requested.")
        
        # Save the updated leave allocation
        leave_allocation.save()

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # When leave request is deleted, restore the balance to the leave allocation
        year = timezone.now().year  # Get the current year
        try:
            leave_allocation = LeaveAllocation.objects.get(teacher=self.teacher, year=year)
        except LeaveAllocation.DoesNotExist:
            raise ValidationError(f"{self.teacher.full_name} does not have a leave allocation for the year {year}.")
        except ObjectDoesNotExist:
            # Handle the case where the teacher doesn't have a leave allocation
            pass
        else:
            if self.status == 'Approved':
                if self.leave_type.name == "Casual Leave":
                    leave_allocation.casual_leave += self.duration
                elif self.leave_type.name == "Sick Leave":
                    leave_allocation.sick_leave += self.duration
                leave_allocation.save()

        super().delete(*args, **kwargs)

    def __str__(self):
        return f"Leave Request by {self.teacher.full_name} for {self.leave_type.name} from {self.from_date} to {self.to_date}"
