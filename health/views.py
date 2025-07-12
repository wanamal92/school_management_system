from django.shortcuts import render, redirect, get_object_or_404
from .models import HealthRecord
from .forms import HealthRecordForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator


def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

def is_admin_or_staff(user):
    return user.is_authenticated and user.role in ['admin', 'staff']

# List all Health Records

@user_passes_test(is_admin_or_staff)
@login_required
def list_health_records(request):
    health_records = HealthRecord.objects.all().order_by('record_type')

    # Pagination setup
    paginator = Paginator(health_records, 10)  # Show 10 students per page
    page_number = request.GET.get('page')
    health_records_page = paginator.get_page(page_number)

    return render(request, 'health/list_health_records.html', {'health_records': health_records_page})

# Create a new Health Record

@user_passes_test(is_admin_or_staff)
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

@user_passes_test(is_admin_or_staff)
@login_required
def update_health_record(request, pk):
    health_record = get_object_or_404(HealthRecord, pk=pk)
    if request.method == 'POST':
        form = HealthRecordForm(request.POST, instance=health_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Health Record updated successfully!")
            return redirect('list_health_records')
        else:
            messages.error(request, "There was an error updating the health record.")
    else:
        form = HealthRecordForm(instance=health_record)
    return render(request, 'health/update_health_record.html', {'form': form})

# Delete a Health Record

@user_passes_test(is_admin)
@login_required
def delete_health_record(request, pk):
    health_record = get_object_or_404(HealthRecord, pk=pk)
    if request.method == 'POST':
        health_record.delete()
        messages.success(request, "Health Record deleted successfully!")
        return redirect('list_health_records')
    return redirect('list_health_records')
