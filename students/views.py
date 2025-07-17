from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from .forms import StudentForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import IntegrityError
from django.contrib import messages
from django.core.paginator import Paginator
from clases.models import Class
from guardians.models import Guardian

def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

def is_admin_or_staff(user):
    return user.is_authenticated and user.role in ['admin', 'staff']


@login_required

def list_students(request):
    # Fetch all students
    students = Student.objects.select_related('user').order_by('full_name')
    classes = Class.objects.all()

    # Apply search filter if a query is present
    # query = request.GET.get('q')
    # if query:
    #     students = students.filter(user__username__icontains=query)

    # # Apply group_by filter if specified (optional)
    # group_by = request.GET.get('group_by')
    # if group_by == "class_level":
    #     students = students.order_by('class_level')

    # Pagination setup
    paginator = Paginator(students, 100)  # Show 10 students per page
    page_number = request.GET.get('page')
    students_page = paginator.get_page(page_number)

    # View mode selection: either list or card view
    view_mode = request.GET.get('view', 'list')


    # Context data
    context = {
        'students': students_page,
        'view_mode': view_mode,
        # 'group_by': group_by,
        'classes': classes
    }

    # Render the list_students template with context data
    return render(request, 'students/list_students.html', context)


@login_required
@user_passes_test(is_admin_or_staff)
def create_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)  # Pass request.FILES to the form

        if form.is_valid():
            try:
                student = form.save(commit=False)  # Save but don't commit to the database
                student.save()  # This will trigger any post-save signals (like user creation)
                messages.success(request, "Student created successfully!")
                return redirect('list_students')
            except IntegrityError as e:
                form.add_error(None, "There was an error with the database. Please try again.")
            except Exception as e:
                form.add_error(None, f"An unexpected error occurred: {e}")
        else:
            # Handle form invalid case (you can also log form.errors for debugging)
            messages.error(request, "There was an error in creating the student.")
            pass
    else:
        form = StudentForm()

    return render(request, 'students/create_student.html', {'form': form})

@login_required
@user_passes_test(is_admin_or_staff)
def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)  # Pass request.FILES to the form
        if form.is_valid():
            form.save()  # Save the student profile along with the profile photo
            messages.success(request, "Student Updated successfully!")
            return redirect('list_students')
        else:
            messages.error(request, "There was an error updating the student.")
    else:
        form = StudentForm(instance=student)

    return render(request, 'students/edit_student.html', {'form': form})


@login_required
@user_passes_test(is_admin)
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    if request.method == 'POST':
        student.delete()
        messages.success(
            request, f'Student {student.full_name} has been deleted successfully.')
        return redirect('list_students')

    return redirect('list_students')


@login_required

def detail_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    return render(request, 'students/detail_student.html', {'student': student})


@login_required
def profile_student(request):
    # Fetch the student's profile related to the logged-in user
    try:
        profile_student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        profile_student = None  # or handle if the profile does not exist

    return render(request, 'students/profile_student.html', {'profile_student': profile_student})

@login_required
def my_childrens(request):
    # Fetch the student's profile related to the logged-in user
    try:
        guardian = Guardian.objects.get(user=request.user)
        students = Student.objects.filter(guardian=guardian)
    except Student.DoesNotExist:
        students = None  # or handle if the profile does not exist

    view_mode = request.GET.get('view', 'list')
    context = {
        'students': students,
        'view_mode': view_mode,
    }

    return render(request, 'students/list_students.html', context)
