from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Duty, TeacherDuty
from .forms import DutyForm, TeacherDutyForm

# View to list all duties
def list_duties(request):
    duties = Duty.objects.all()
    return render(request, 'dutymanagement/list_duties.html', {'duties': duties})

# View to create a new duty
def create_duty(request):
    if request.method == 'POST':
        form = DutyForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Duty created successfully.")
            return redirect('list_duties')
    else:
        form = DutyForm()
    return render(request, 'dutymanagement/create_duty.html', {'form': form})

# View to edit an existing duty
def edit_duty(request, pk):
    duty = get_object_or_404(Duty, pk=pk)
    if request.method == 'POST':
        form = DutyForm(request.POST, instance=duty)
        if form.is_valid():
            form.save()
            messages.success(request, "Duty updated successfully.")
            return redirect('list_duties')
    else:
        form = DutyForm(instance=duty)
    return render(request, 'dutymanagement/edit_duty.html', {'form': form})

# View to delete a duty
def delete_duty(request, pk):
    duty = get_object_or_404(Duty, pk=pk)
    duty.delete()
    messages.success(request, "Duty deleted successfully.")
    return redirect('list_duties')

# View to list all teacher duties
def list_teacher_duties(request):
    teacher_duties = TeacherDuty.objects.all()
    return render(request, 'dutymanagement/list_teacher_duties.html', {'teacher_duties': teacher_duties})

# View to create a new teacher duty
def create_teacher_duty(request):
    if request.method == 'POST':
        form = TeacherDutyForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Teacher duty assigned successfully.")
            return redirect('list_teacher_duties')
    else:
        form = TeacherDutyForm()
    return render(request, 'dutymanagement/create_teacher_duty.html', {'form': form})

# View to edit an existing teacher duty
def edit_teacher_duty(request, pk):
    teacher_duty = get_object_or_404(TeacherDuty, pk=pk)
    if request.method == 'POST':
        form = TeacherDutyForm(request.POST, instance=teacher_duty)
        if form.is_valid():
            form.save()
            messages.success(request, "Teacher duty updated successfully.")
            return redirect('list_teacher_duties')
    else:
        form = TeacherDutyForm(instance=teacher_duty)
    return render(request, 'dutymanagement/edit_teacher_duty.html', {'form': form})

# View to delete a teacher duty
def delete_teacher_duty(request, pk):
    teacher_duty = get_object_or_404(TeacherDuty, pk=pk)
    teacher_duty.delete()
    messages.success(request, "Teacher duty deleted successfully.")
    return redirect('list_teacher_duties')
