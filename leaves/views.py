from django.shortcuts import render, redirect, get_object_or_404
from .models import LeaveRequest, LeaveAllocation, LeaveType
from .forms import LeaveRequestForm, LeaveAllocationForm, LeaveTypeForm
from django.contrib.auth.decorators import login_required, user_passes_test

def is_admin(user):
    return user.is_superuser  # Admin check


@user_passes_test(is_admin)
def list_leave_types(request):
    leave_types = LeaveType.objects.all()  # Fetch all leave types
    return render(request, 'leaves/list_leave_types.html', {'leave_types': leave_types})

# Create Leave Type
@user_passes_test(is_admin)
def create_leave_type(request):
    if request.method == 'POST':
        form = LeaveTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_leave_types')
    else:
        form = LeaveTypeForm()
    return render(request, 'leaves/create_leave_type.html', {'form': form})

# Create Leave Allocation
@user_passes_test(is_admin)
def create_leave_allocation(request):
    if request.method == 'POST':
        form = LeaveAllocationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('leave_allocation')  # Redirect after creating leave allocation
    else:
        form = LeaveAllocationForm()
    return render(request, 'leaves/create_leave_allocation.html', {'form': form})

# Teacher Leave Request List (View and Apply Leave)
@login_required
def teacher_leave_requests(request):
    teacher = request.user.teacher  # Assuming user is related to teacher model
    leave_requests = LeaveRequest.objects.filter(teacher=teacher)
    leave_allocation = LeaveAllocation.objects.get(teacher=teacher)
    return render(request, 'leaves/teacher_leave_requests.html', {
        'leave_requests': leave_requests,
        'leave_allocation': leave_allocation
    })

# Admin View to List All Leave Requests
@user_passes_test(is_admin)
def admin_leave_requests(request):
    leave_requests = LeaveRequest.objects.all()
    return render(request, 'leaves/admin_leave_requests.html', {'leave_requests': leave_requests})

# Create Leave Request (Teacher applies for leave)
@login_required
def create_leave_request(request):
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave_request = form.save(commit=False)
            leave_request.teacher = request.user.teacher  # Assign teacher automatically
            leave_request.save()
            return redirect('teacher_leave_requests')  # Redirect to leave requests list
    else:
        form = LeaveRequestForm()
    return render(request, 'leaves/create_leave_request.html', {'form': form})

# Admin can approve or reject leave requests
@user_passes_test(is_admin)
def approve_reject_leave(request, pk):
    leave_request = get_object_or_404(LeaveRequest, pk=pk)
    if request.method == 'POST':
        leave_request.status = request.POST.get('status')
        leave_request.save()
        return redirect('admin_leave_requests')
    return render(request, 'leaves/approve_reject_leave.html', {'leave_request': leave_request})

# Admin View for Leave Allocation
@user_passes_test(is_admin)
def leave_allocation(request):
    leave_allocations = LeaveAllocation.objects.all()
    return render(request, 'leaves/leave_allocation.html', {'leave_allocations': leave_allocations})

# Update Leave Allocation
@user_passes_test(is_admin)
def update_leave_allocation(request, pk):
    leave_allocation = get_object_or_404(LeaveAllocation, pk=pk)
    if request.method == 'POST':
        form = LeaveAllocationForm(request.POST, instance=leave_allocation)
        if form.is_valid():
            form.save()
            return redirect('leave_allocation')
    else:
        form = LeaveAllocationForm(instance=leave_allocation)
    return render(request, 'leaves/update_leave_allocation.html', {'form': form})


@login_required
def delete_leave_request(request, pk):
    leave_request = get_object_or_404(LeaveRequest, pk=pk)
    if leave_request.status == 'Approved':
        # Restore the leave balance if request was approved
        if leave_request.leave_type.name == "Casual Leave":
            leave_request.teacher.leaveallocation.casual_leave += leave_request.duration
        elif leave_request.leave_type.name == "Sick Leave":
            leave_request.teacher.leaveallocation.sick_leave += leave_request.duration
        leave_request.teacher.leaveallocation.save()

    leave_request.delete()  # Delete the leave request
    return redirect('teacher_leave_requests')  # Redirect back to leave requests list
