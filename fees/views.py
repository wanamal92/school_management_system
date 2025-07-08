from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import FeeType, FeePayment
from .forms import FeePaymentForm,FeeTypeForm

# List all fee payments
def list_fee_payments(request):
    payments = FeePayment.objects.all()
    return render(request, 'fees/list_fee_payments.html', {'payments': payments})

# Create new fee payment
def create_fee_payment(request):
    if request.method == 'POST':
        form = FeePaymentForm(request.POST)
        if form.is_valid():
            form.save()  # Save the fee payment, balance and status will be auto-calculated
            messages.success(request, 'Fee Payment added successfully!')
            return redirect('list_fee_payments')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = FeePaymentForm()

    return render(request, 'fees/create_fee_payment.html', {'form': form})

# Edit fee payment
def edit_fee_payment(request, pk):
    payment = get_object_or_404(FeePayment, pk=pk)
    if request.method == 'POST':
        form = FeePaymentForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()  # This will automatically update the balance and status
            messages.success(request, 'Fee Payment updated successfully!')
            return redirect('list_fee_payments')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = FeePaymentForm(instance=payment)

    return render(request, 'fees/edit_fee_payment.html', {'form': form})

# Delete fee payment
def delete_fee_payment(request, pk):
    payment = get_object_or_404(FeePayment, pk=pk)
    payment.delete()
    messages.success(request, 'Fee Payment deleted successfully!')
    return redirect('list_fee_payments')



# List all fee types
def list_fee_types(request):
    fee_types = FeeType.objects.all()
    return render(request, 'fees/list_fee_types.html', {'fee_types': fee_types})

# Create new fee type
def create_fee_type(request):
    if request.method == 'POST':
        form = FeeTypeForm(request.POST)
        if form.is_valid():
            form.save()  
            messages.success(request, 'Fee Type added successfully!')
            return redirect('list_fee_types')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = FeePaymentForm()
    return render(request, 'fees/create_fee_type.html')

# Edit fee type
def edit_fee_type(request, pk):
    fee_type = get_object_or_404(FeeType, pk=pk)
    if request.method == 'POST':
        
        if request.method == 'POST':
            form = FeeTypeForm(request.POST, instance=fee_type)
            if form.is_valid():
                form.save()  
                messages.success(request, 'Fee Type updated successfully!')
                return redirect('list_fee_types')
            else:
                messages.error(request, 'Please correct the errors below.')
        else:
            form = FeeTypeForm(instance=fee_type)

    return render(request, 'fees/edit_fee_type.html', {'fee_type': fee_type})

# Delete fee type
def delete_fee_type(request, pk):
    fee_type = get_object_or_404(FeeType, pk=pk)
    fee_type.delete()
    messages.success(request, 'Fee Type deleted successfully!')
    return redirect('list_fee_types')
