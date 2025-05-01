from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from .forms import StudentForm
from django.contrib.auth.decorators import login_required, user_passes_test

def is_admin_or_staff(user):
    return user.is_authenticated and user.role in ['admin', 'staff']

@login_required
@user_passes_test(is_admin_or_staff)
def student_list(request):
    students = Student.objects.select_related('user')
    view_mode = request.GET.get('view', 'list')
    query = request.GET.get('q')
    if query:
        students = students.filter(user__username__icontains=query)
    group_by = request.GET.get('group_by')
    context = {'students': students, 'view_mode': view_mode, 'group_by': group_by}
    return render(request, 'students/student_list.html', context)

@login_required
@user_passes_test(is_admin_or_staff)
def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'students/student_form.html', {'form': form})

@login_required
@user_passes_test(is_admin_or_staff)
def student_edit(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'students/student_form.html', {'form': form})

@login_required
@user_passes_test(is_admin_or_staff)
def student_delete(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    student.delete()
    return redirect('student_list')

@login_required
@user_passes_test(is_admin_or_staff)
def student_detail(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    return render(request, 'students/student_detail.html', {'student': student})

