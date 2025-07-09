from django import forms
from .models import FeePayment, FeeType, Student


class FeeTypeForm(forms.ModelForm):
    class Meta:
        model = FeeType
        fields = ['name', 'amount']


class FeePaymentForm(forms.ModelForm):
    class Meta:
        model = FeePayment
        fields = ['student', 'fee_type', 'paid_amount', 'year']

    def clean_paid_amount(self):
        paid_amount = self.cleaned_data.get('paid_amount')
        fee_type = self.cleaned_data.get('fee_type')

        # Check if the paid amount is greater than the total fee amount
        if paid_amount > fee_type.amount:
            raise forms.ValidationError(
                "Paid amount cannot be greater than the total fee amount.")

        return paid_amount
