from django.db import models
from teachers.models import Teacher
from django.db.models import F


class LeaveType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class LeaveAllocation(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    casual_leave = models.IntegerField(
        default=14)  # 14 days casual leave annually
    sick_leave = models.IntegerField(default=7)  # 7 days sick leave annually
    year = models.PositiveIntegerField()

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
    # Duration will be calculated
    duration = models.IntegerField(blank=True, null=True)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), (
        'Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending')

    def save(self, *args, **kwargs):
        # Automatically calculate duration based on from_date and to_date
        if self.from_date and self.to_date:
            self.duration = (self.to_date - self.from_date).days + 1
        super().save(*args, **kwargs)

        # Update leave allocation balance
        if self.status == 'Approved':
            if self.leave_type.name == "Casual Leave":
                self.teacher.leaveallocation.casual_leave -= self.duration
            elif self.leave_type.name == "Sick Leave":
                self.teacher.leaveallocation.sick_leave -= self.duration
            self.teacher.leaveallocation.save()

    def delete(self, *args, **kwargs):
        # When leave request is deleted, restore the balance to the leave allocation
        if self.status == 'Approved':
            if self.leave_type.name == "Casual Leave":
                self.teacher.leaveallocation.casual_leave += self.duration
            elif self.leave_type.name == "Sick Leave":
                self.teacher.leaveallocation.sick_leave += self.duration
            self.teacher.leaveallocation.save()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"Leave Request by {self.teacher.full_name} for {self.leave_type.name} from {self.from_date} to {self.to_date}"
