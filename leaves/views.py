from django.shortcuts import render, redirect, get_object_or_404
from .models import LeaveRequest, LeaveAllocation, LeaveType
from .forms import LeaveRequestForm, LeaveAllocationForm, LeaveTypeForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.contrib import messages
from teachers.models import Teacher


def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

def is_admin_or_staff(user):
    return user.is_authenticated and user.role in ['admin', 'staff']


@user_passes_test(is_admin)
@login_required
def list_leave_types(request):
    leave_types = LeaveType.objects.all().order_by('name')  # Fetch all leave types

    # Pagination setup
    paginator = Paginator(leave_types, 10)  # Show 10 students per page
    page_number = request.GET.get('page')
    leave_types_page = paginator.get_page(page_number)

    return render(request, 'leaves/list_leave_types.html', {'leave_types': leave_types_page})

# Create Leave Type


@user_passes_test(is_admin)
@login_required
def create_leave_type(request):
    if request.method == 'POST':
        form = LeaveTypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Leave Type created successfully!")
            return redirect('list_leave_types')
        else:
            messages.error(request, "There was an error in creating the leave type.")
    else:
        form = LeaveTypeForm()
    return render(request, 'leaves/create_leave_type.html', {'form': form})

# Edit Leave Type

@user_passes_test(is_admin)
@login_required
def edit_leave_type(request, pk):
    leave_type = get_object_or_404(LeaveType, pk=pk)
    if request.method == 'POST':
        form = LeaveTypeForm(request.POST, instance=leave_type)
        if form.is_valid():
            form.save()
            messages.success(request, "Leave Type updated successfully.")
            return redirect('list_leave_types')
        else:
            messages.error(request, "There was an error updating the leave type.")
    else:
        form = LeaveTypeForm(instance=leave_type)
    return render(request, 'leaves/edit_leave_type.html', {'form': form})

# Delete Leave Type


@user_passes_test(is_admin)
@login_required
def delete_leave_type(request, pk):
    leave_type = get_object_or_404(LeaveType, pk=pk)
    if request.method == 'POST':
        leave_type.delete()  #
        messages.success(request, "Leave Type deleted successfully!")
        return redirect('list_leave_types')
    return redirect('list_leave_types')

# Leave Allocation List


@login_required
@user_passes_test(is_admin)
def list_leave_allocations(request):
    leave_allocations = LeaveAllocation.objects.all().order_by('teacher__full_name')

    # Pagination setup
    paginator = Paginator(leave_allocations, 10)  # Show 10 students per page
    page_number = request.GET.get('page')
    leave_allocations_page = paginator.get_page(page_number)

    return render(request, 'leaves/list_leave_allocations.html', {'leave_allocations': leave_allocations_page})

# Create Leave Allocation


@login_required
@user_passes_test(is_admin)
def create_leave_allocation(request):
    if request.method == 'POST':
        form = LeaveAllocationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Leave Allocation created successfully!")
            return redirect('list_leave_allocations')  # Redirect after saving the form
        else:
            messages.error(request, "There was an error in creating the leave allocation.")
            # Pass form with errors back to template
            return render(request, 'leaves/create_leave_allocation.html', {'form': form})
    else:
        form = LeaveAllocationForm()
    
    return render(request, 'leaves/create_leave_allocation.html', {'form': form})

# Update Leave Allocation


@login_required
@user_passes_test(is_admin)
def edit_leave_allocation(request, pk):
    leave_allocation = get_object_or_404(LeaveAllocation, pk=pk)
    if request.method == 'POST':
        form = LeaveAllocationForm(request.POST, instance=leave_allocation)
        if form.is_valid():
            form.save()
            messages.success(request, "Leave Allocation updated successfully!")
            return redirect('list_leave_allocations')
        else:
            messages.error(request, "There was an error updating the leave allocation.")
    else:
        form = LeaveAllocationForm(instance=leave_allocation)
    return render(request, 'leaves/edit_leave_allocation.html', {'form': form})

# Delete Leave Allocation

@user_passes_test(is_admin)
@login_required
def delete_leave_allocation(request, pk):
    leave_allocation = get_object_or_404(LeaveAllocation, pk=pk)
    if request.method == 'POST':
        leave_allocation.delete()  #
        messages.success(request, "Leave Allocation deleted successfully!")
        return redirect('list_leave_allocations')
    return redirect('list_leave_allocations')

# Admin View to List All Leave Requests


@login_required
@user_passes_test(is_admin)
def admin_leave_requests(request):
    leave_requests = LeaveRequest.objects.all().order_by('teacher__full_name')

    # Pagination setup
    paginator = Paginator(leave_requests, 10)  # Show 10 students per page
    page_number = request.GET.get('page')
    leave_requests_page = paginator.get_page(page_number)

    return render(request, 'leaves/admin_leave_requests.html', {'leave_requests': leave_requests_page})

# Admin can approve or reject leave requests


@login_required
@user_passes_test(is_admin)
def approve_reject_leave(request, pk):
    leave_request = get_object_or_404(LeaveRequest, pk=pk)
    if request.method == 'POST':
        leave_request.status = request.POST.get('status')
        leave_request.save()
        messages.success(request, "Leave Request updated successfully!")
        return redirect('admin_leave_requests')
    else:
            messages.error(request, "There was an error updating the leave request.")
    return render(request, 'leaves/approve_reject_leave.html', {'leave_request': leave_request})


# Teacher Leave Request List (View and Apply Leave)
@user_passes_test(is_admin_or_staff)
@login_required
def teacher_leave_requests(request):
    # Fetch the teacher object linked to the logged-in user
     # Assuming user is related to teacher model
    teacher = Teacher.objects.get(user=request.user)

    leave_requests = LeaveRequest.objects.filter(
        teacher=teacher).order_by('teacher__full_name')
    leave_allocation = LeaveAllocation.objects.get(teacher=teacher)

    # Pagination setup
    paginator = Paginator(leave_requests, 10)  # Show 10 leave requests per page
    page_number = request.GET.get('page')
    leave_requests_page = paginator.get_page(page_number)

    # Pass the teacher object to the form so it can pre-fill the teacher field
    form = LeaveRequestForm(user=request.user)  # Pass the user to the form to set the teacher field

    return render(request, 'leaves/teacher_leave_requests.html', {
        'leave_requests': leave_requests_page,
        'leave_allocation': leave_allocation,
        'teacher': teacher,
        'form': form  # Pass the form to the template
    })


# Create Leave Request (Teacher applies for leave)
@user_passes_test(is_admin_or_staff)
@login_required
def create_leave_request(request):
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave_request = form.save(commit=False)
            leave_request.save()
            messages.success(request, "Leave Request created successfully!")
            
            # Redirect to the appropriate leave request page based on role
            if request.user.role == 'admin':
                return redirect('admin_leave_requests')
            elif request.user.role == 'staff':
                return redirect('teacher_leave_requests')
        else:
            messages.error(request, "There was an error in creating the leave request.")
    else:
        

        form = LeaveRequestForm(user=request.user)  

    return render(request, 'leaves/create_leave_request.html', {'form': form})

# Update Leave Request

@user_passes_test(is_admin_or_staff)
@login_required
def edit_leave_request(request, pk):
    leave_request = get_object_or_404(LeaveRequest, pk=pk)
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST, instance=leave_request)
        if form.is_valid():
            form.save()
            messages.success(request, "Leave Request updated successfully!")
            
            if request.user.role == 'admin':
                
                return redirect('admin_leave_requests')  
            elif request.user.role == 'staff':
                
                return redirect('teacher_leave_requests')
        else:
            messages.error(request, "There was an error updating the leave request.")
    else:
        form = LeaveRequestForm(instance=leave_request,user=request.user)
    return render(request, 'leaves/edit_leave_request.html', {'form': form})


# Delete Leave Request
@user_passes_test(is_admin_or_staff)
@login_required
def delete_leave_request(request, pk):
    leave_request = get_object_or_404(LeaveRequest, pk=pk)
    if request.method == 'POST':
        if leave_request.status == 'Approved':
            # Restore the leave balance if request was approved
            if leave_request.leave_type.name == "Casual Leave":
                leave_request.teacher.leaveallocation.casual_leave += leave_request.duration
            elif leave_request.leave_type.name == "Sick Leave":
                leave_request.teacher.leaveallocation.sick_leave += leave_request.duration
            leave_request.teacher.leaveallocation.save()

        leave_request.delete()  # Delete the leave request
        messages.success(request, "Leave Request deleted successfully!")
        if request.user.role == 'admin':
                
            return redirect('admin_leave_requests')  
        elif request.user.role == 'staff':
                
            return redirect('teacher_leave_requests')
    # Redirect back to leave requests list
    if request.user.role == 'admin':
                
        return redirect('admin_leave_requests')  
    elif request.user.role == 'staff':
                
        return redirect('teacher_leave_requests')
