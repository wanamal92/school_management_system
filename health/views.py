from django.shortcuts import render, redirect, get_object_or_404
from .models import HealthRecord
from .forms import HealthRecordForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# List all Health Records
@login_required
def list_health_records(request):
    health_records = HealthRecord.objects.all()
    return render(request, 'health/list_health_records.html', {'health_records': health_records})

# Create a new Health Record
@login_required
def create_health_record(request):
    if request.method == 'POST':
        form = HealthRecordForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Health record created successfully!')
            return redirect('list_health_records')  # Adjust URL name as needed
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = HealthRecordForm()
    
    return render(request, 'health/create_health_record.html', {'form': form})

# Update an existing Health Record
@login_required
def update_health_record(request, pk):
    health_record = get_object_or_404(HealthRecord, pk=pk)
    if request.method == 'POST':
        form = HealthRecordForm(request.POST, instance=health_record)
        if form.is_valid():
            form.save()
            return redirect('list_health_records')
    else:
        form = HealthRecordForm(instance=health_record)
    return render(request, 'health/update_health_record.html', {'form': form})

# Delete a Health Record
@login_required
def delete_health_record(request, pk):
    health_record = get_object_or_404(HealthRecord, pk=pk)
    if request.method == 'POST':
        health_record.delete()
        return redirect('list_health_records')
    return render(request, 'health/delete_health_record.html', {'health_record': health_record})
