from django import forms
from .models import FeePayment, FeeType, Student
from django.core.exceptions import ValidationError


class FeeTypeForm(forms.ModelForm):
    class Meta:
        model = FeeType
        fields = ['name', 'amount']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

        # Custom validation for 'name'
    def clean_name(self):
        name = self.cleaned_data.get('name')
        
        # Ensure the name is not empty
        if not name:
            raise ValidationError("Fee name cannot be empty.")
        
        # Ensure the name is not too long
        if len(name) > 255:
            raise ValidationError("Fee name cannot be longer than 255 characters.")
        
        return name

    # Custom validation for 'amount'
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')

        # Ensure the amount is positive
        if amount <= 0:
            raise ValidationError("Fee amount must be a positive number.")
        
        return amount


class FeePaymentForm(forms.ModelForm):
    class Meta:
        model = FeePayment
        fields = ['student', 'fee_type', 'paid_amount', 'year']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    # Custom validation for 'paid_amount'
    def clean_paid_amount(self):
        paid_amount = self.cleaned_data.get('paid_amount')
        fee_type = self.cleaned_data.get('fee_type')

        if paid_amount < 0:
            raise forms.ValidationError("Paid amount cannot be negative.")

        # Check if the paid amount is greater than the total fee amount
        if paid_amount > fee_type.amount:
            raise forms.ValidationError("Paid amount cannot be greater than the total fee amount.")

        return paid_amount

    # Optionally, you could validate if the year field is within a valid range
    def clean_year(self):
        year = self.cleaned_data.get('year')
        if not (1900 <= year <= 2100):  # Allow only valid years
            raise ValidationError("Year must be between 1900 and 2100.")
        return year

    # Custom validation for 'fee_type' to ensure a valid fee type is selected
    def clean_fee_type(self):
        fee_type = self.cleaned_data.get('fee_type')
        if not FeeType.objects.filter(id=fee_type.id).exists():
            raise ValidationError("The selected fee type does not exist.")
        return fee_type

    def save(self, *args, **kwargs):
        # Saving the form and calculating balance and status
        instance = super().save(commit=False)
        instance.balance = instance.fee_type.amount - instance.paid_amount
        
        if instance.balance == 0:
            instance.status = 'Paid'
        elif instance.balance < instance.fee_type.amount:
            instance.status = 'Partially'
        else:
            instance.status = 'Pending'
        
        instance.save()  # Save the fee payment instance with updated balance and status
        return instance
