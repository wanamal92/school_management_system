from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Duty, TeacherDuty
from .forms import DutyForm, TeacherDutyForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, user_passes_test

# View to list all duties

def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

def is_admin_or_staff(user):
    return user.is_authenticated and user.role in ['admin', 'staff']

@user_passes_test(is_admin_or_staff)
@login_required
def list_duties(request):
    duties = Duty.objects.all().order_by('name')

    # Pagination setup
    paginator = Paginator(duties, 10)  # Show 10 students per page
    page_number = request.GET.get('page')
    duties_page = paginator.get_page(page_number)

    return render(request, 'duties/list_duties.html', {'duties': duties_page})

# View to create a new duty

@user_passes_test(is_admin)
@login_required
def create_duty(request):
    if request.method == 'POST':
        form = DutyForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Duty created successfully.")
            return redirect('list_duties')
        else:
            messages.error(request, "There was an error in creating the duty.")       
    else:
        form = DutyForm()
    return render(request, 'duties/create_duty.html', {'form': form})

# View to edit an existing duty

@user_passes_test(is_admin)
@login_required
def edit_duty(request, pk):
    duty = get_object_or_404(Duty, pk=pk)
    if request.method == 'POST':
        form = DutyForm(request.POST, instance=duty)
        if form.is_valid():
            form.save()
            messages.success(request, "Duty updated successfully.")
            return redirect('list_duties')
        else:
            messages.error(request, "There was an error updating the duty.")
    else:
        form = DutyForm(instance=duty)
    return render(request, 'duties/edit_duty.html', {'form': form})

# View to delete a duty

@user_passes_test(is_admin)
@login_required
def delete_duty(request, pk):
    duty = get_object_or_404(Duty, pk=pk)
    if request.method == 'POST':
        duty.delete()
        messages.success(request, "Duty deleted successfully.")
        return redirect('list_duties')
    return redirect('list_duties')


# View to list all teacher duties
@user_passes_test(is_admin_or_staff)
def list_teacher_duties(request):
    teacher_duties = TeacherDuty.objects.all().order_by('teacher__full_name')

    # Pagination setup
    paginator = Paginator(teacher_duties, 10)  # Show 10 students per page
    page_number = request.GET.get('page')
    teacher_duties_page = paginator.get_page(page_number)

    return render(request, 'duties/list_teacher_duties.html', {'teacher_duties': teacher_duties_page})

# View to create a new teacher duty

@user_passes_test(is_admin)
def create_teacher_duty(request):
    if request.method == 'POST':
        form = TeacherDutyForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Teacher duty assigned successfully.")
            return redirect('list_teacher_duties')
        else:
            messages.error(request, "There was an error in creating the Teacher duty.")
    else:
        form = TeacherDutyForm()
    return render(request, 'duties/create_teacher_duty.html', {'form': form})

# View to edit an existing teacher duty

@user_passes_test(is_admin)
def edit_teacher_duty(request, pk):
    teacher_duty = get_object_or_404(TeacherDuty, pk=pk)
    if request.method == 'POST':
        form = TeacherDutyForm(request.POST, instance=teacher_duty)
        if form.is_valid():
            form.save()
            messages.success(request, "Teacher duty updated successfully.")
            return redirect('list_teacher_duties')
        else:
            messages.error(request, "There was an error updating the Teacher duty.")
    else:
        form = TeacherDutyForm(instance=teacher_duty)
    return render(request, 'duties/edit_teacher_duty.html', {'form': form})

# View to delete a teacher duty

@user_passes_test(is_admin)
def delete_teacher_duty(request, pk):
    teacher_duty = get_object_or_404(TeacherDuty, pk=pk)
    if request.method == 'POST':
        teacher_duty.delete()
        messages.success(request, "Teacher duty deleted successfully.")
        return redirect('list_teacher_duties')
    return redirect('list_teacher_duties')
