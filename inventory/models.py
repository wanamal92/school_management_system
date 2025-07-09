from django.db import models
from teachers.models import Teacher
from django.utils import timezone

# Category model to categorize items


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

# Item model to store inventory items


class Item(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('in_use', 'In Use'),
        ('out_of_stock', 'Out of Stock'),
    ]

    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    status = models.CharField(
        max_length=15, choices=STATUS_CHOICES, default='available')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    added_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.name} - {self.category.name}"

    def increase_stock(self, quantity):
        self.quantity += quantity
        self.save()

    def decrease_stock(self, quantity):
        if self.quantity >= quantity:
            self.quantity -= quantity
            self.save()
        else:
            raise ValueError("Not enough stock to decrease")

# TeacherItem model to assign items to teachers


class TeacherItem(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    assigned_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.teacher} - {self.item} - {self.quantity}"

    def save(self, *args, **kwargs):
        # Ensure that the quantity is deducted from the Item when assigning it to a teacher
        item = self.item
        if item.quantity >= self.quantity:
            item.decrease_stock(self.quantity)  # Deduct stock from the item
            super().save(*args, **kwargs)
        else:
            raise ValueError(
                f"Not enough stock of {item.name} to assign {self.quantity} to {self.teacher}")
