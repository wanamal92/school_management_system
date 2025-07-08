from django.db import models
from students.models import Student



class FeeType(models.Model):
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class FeePayment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    fee_type = models.ForeignKey(FeeType, on_delete=models.CASCADE)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status_choices = [
        ('Paid', 'Paid'),
        ('Pending', 'Pending'),
        ('Partially', 'Partially')
    ]
    status = models.CharField(max_length=10, choices=status_choices, default='Pending')
    year = models.PositiveIntegerField()  # New field to store the year of the fee payment

    def save(self, *args, **kwargs):
        # Calculate balance and update status when the fee payment is saved
        self.balance = self.fee_type.amount - self.paid_amount

        if self.balance == 0:
            self.status = 'Paid'
        elif self.balance < self.fee_type.amount:
            self.status = 'Partially'
        else:
            self.status = 'Pending'

        super().save(*args, **kwargs)  # Save the object

    def __str__(self):
        return f'{self.student.name} - {self.fee_type.name} ({self.year})'
