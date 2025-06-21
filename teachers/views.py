# teachers/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Teacher
from .forms import TeacherForm
from django.contrib.auth.decorators import login_required, user_passes_test


def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

# List all teachers
@user_passes_test(is_admin)
@login_required
def teacher_list(request):
    # Get the view mode from the URL parameter (default is 'list')
    view_mode = request.GET.get('view', 'list')
    
    # Fetch all the teachers (you can modify this query based on your needs)
    teachers = Teacher.objects.all()
    
    # Pass the teachers and view_mode to the template
    return render(request, 'teachers/teacher_list.html', {
        'teachers': teachers,
        'view_mode': view_mode,
    })

# Add a new teacher
@user_passes_test(is_admin)
@login_required
def add_teacher(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('teacher_list')
    else:
        form = TeacherForm()
    return render(request, 'teachers/add_teacher.html', {'form': form})

# Edit an existing teacher
@user_passes_test(is_admin)
@login_required
def edit_teacher(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == 'POST':
        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            return redirect('teacher_list')
    else:
        form = TeacherForm(instance=teacher)
    return render(request, 'teachers/edit_teacher.html', {'form': form})

# Delete a teacher
@user_passes_test(is_admin)
@login_required
def delete_teacher(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == 'POST':
        teacher.delete()
        return redirect('teacher_list')
    return render(request, 'teachers/delete_teacher.html', {'teacher': teacher})

@user_passes_test(is_admin)
@login_required
def teacher_detail(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    return render(request, 'teachers/teacher_detail.html', {'teacher': teacher})
