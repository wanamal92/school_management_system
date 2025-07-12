from django import forms
from .models import Item, Category, TeacherItem
from teachers.models import Teacher
from django.core.exceptions import ValidationError
from django.utils import timezone


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    # Custom validation for 'name' field
    def clean_name(self):
        name = self.cleaned_data.get('name')

        # Ensure the name is not empty
        if not name:
            raise ValidationError("Category name cannot be empty.")
        
        # Ensure the name is not too long
        if len(name) > 255:
            raise ValidationError("Category name cannot be longer than 255 characters.")

        # Ensure the name is unique
        if Category.objects.exclude(id=self.instance.id).filter(name=name).exists():
            raise ValidationError(f"The category '{name}' already exists. Please choose a different name.")
        
        return name

# Form to create/update Item


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'category', 'quantity',
                  'status', 'price', 'description', 'added_date']
    

        widgets = {
            'added_date': forms.DateInput(attrs={'type': 'date'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    # Custom validation for 'name'
    def clean_name(self):
        name = self.cleaned_data.get('name')
        
        # Ensure the name is not empty
        if not name:
            raise ValidationError("Item name cannot be empty.")
        
        # Ensure the name is not too long
        if len(name) > 255:
            raise ValidationError("Item name cannot be longer than 255 characters.")
        
        return name

    # Custom validation for 'quantity'
    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')

        # Ensure quantity is a positive integer
        if quantity < 0:
            raise ValidationError("Quantity must be a positive integer.")
        
        return quantity

    # Custom validation for 'price'
    def clean_price(self):
        price = self.cleaned_data.get('price')

        # Ensure price is a positive number
        if price <= 0:
            raise ValidationError("Price must be greater than zero.")
        
        return price

    # Custom validation for 'status'
    def clean_status(self):
        status = self.cleaned_data.get('status')

        # Ensure the status is valid
        if status not in dict(Item.STATUS_CHOICES):
            raise ValidationError("Invalid status. Please select a valid status.")
        
        return status

    # Custom validation for 'description'
    def clean_description(self):
        description = self.cleaned_data.get('description')

        # Ensure description is not too long (optional)
        if description and len(description) > 1000:
            raise ValidationError("Description cannot exceed 1000 characters.")
        
        return description


# Form to create/update TeacherItem (assign items to teachers)
class TeacherItemForm(forms.ModelForm):
    class Meta:
        model = TeacherItem
        fields = ['teacher', 'item', 'quantity', 'assigned_date']


        widgets = {
            'assigned_date': forms.DateInput(attrs={'type': 'date'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    # Custom validation for 'quantity'
    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        item = self.cleaned_data.get('item')

        # Ensure that quantity is positive
        if quantity <= 0:
            raise ValidationError("Quantity must be a positive integer.")

        # Ensure that the quantity does not exceed the available stock in the item
        if item.quantity < quantity:
            raise ValidationError(
                f"Not enough stock of {item.name}. Only {item.quantity} are available."
            )

        return quantity

    # Custom validation for 'assigned_date'
    def clean_assigned_date(self):
        assigned_date = self.cleaned_data.get('assigned_date')

        # Ensure that the assigned date is not in the future
        if assigned_date > timezone.now().date():
            raise ValidationError("Assigned date cannot be in the future.")
        
        return assigned_date

    # Additional save logic can be applied here for custom actions before saving
    # def save(self, *args, **kwargs):
    #     instance = super().save(commit=False)
        
    #     # Deduct the stock when the item is assigned to the teacher
    #     item = instance.item
    #     if item.quantity >= instance.quantity:
    #         item.decrease_stock(instance.quantity)  # Deduct stock from the item
    #         instance.save()
    #     else:
    #         raise ValueError(
    #             f"Not enough stock of {item.name} to assign {instance.quantity} to {instance.teacher}"
    #         )

    #     return instance
