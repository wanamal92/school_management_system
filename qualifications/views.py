# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import TeacherQualification, Qualification, Teacher
from .forms import TeacherQualificationForm, QualificationForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator

# List View with filtering


@login_required
def list_teacher_qualifications(request):
    qualifications = TeacherQualification.objects.all().order_by('teacher')

    teacher_name = request.GET.get('teacher')
    qualification_name = request.GET.get('qualification')

    if teacher_name:
        qualifications = qualifications.filter(
            teacher__full_name__icontains=teacher_name)
    if qualification_name:
        qualifications = qualifications.filter(
            qualification__name__icontains=qualification_name)

    # Pagination setup
    paginator = Paginator(qualifications, 10)  # Show 10 students per page
    page_number = request.GET.get('page')
    qualifications_page = paginator.get_page(page_number)

    return render(request, 'qualifications/list_teacher_qualifications.html', {
        'qualifications': qualifications_page,
        'teacher_name': teacher_name,
        'qualification_name': qualification_name
    })


# Create View
@login_required
def create_teacher_qualification(request):
    if request.method == 'POST':
        form = TeacherQualificationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Teacher qualification added successfully!')
            return redirect('list_teacher_qualifications')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TeacherQualificationForm()

    return render(request, 'qualifications/create_teacher_qualification.html', {'form': form})

# Edit View


@login_required
def edit_teacher_qualification(request, pk):
    teacher_qualification = get_object_or_404(TeacherQualification, pk=pk)
    if request.method == 'POST':
        form = TeacherQualificationForm(
            request.POST, instance=teacher_qualification)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Teacher qualification updated successfully!')
            return redirect('list_teacher_qualifications')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TeacherQualificationForm(instance=teacher_qualification)

    return render(request, 'qualifications/edit_teacher_qualification.html', {'form': form})

# Delete View


@login_required
def delete_teacher_qualification(request, pk):
    teacher_qualification = get_object_or_404(TeacherQualification, pk=pk)
    if request.method == 'POST':
        teacher_qualification.delete()
        return redirect('list_teacher_qualifications')
    return redirect('list_teacher_qualifications')


@login_required
def list_qualifications(request):
    qualifications = Qualification.objects.all()  # Get all qualifications initially

    # Get the search term from the GET parameters
    qualification_name = request.GET.get('qualification_name')

    # If the qualification name filter is provided, apply the filter
    if qualification_name:
        qualifications = qualifications.filter(
            name__icontains=qualification_name)

    # Pagination setup
    paginator = Paginator(qualifications, 10) 
    page_number = request.GET.get('page')
    qualifications_page = paginator.get_page(page_number)

    # Render the qualifications list page with the filtered qualifications
    return render(request, 'qualifications/list_qualifications.html', {
        'qualifications': qualifications_page,
        'qualification_name': qualification_name
    })

# Create Qualification View


@login_required
def create_qualification(request):
    if request.method == 'POST':
        form = QualificationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Qualification added successfully!')
            return redirect('list_qualifications')
    else:
        form = QualificationForm()
    return render(request, 'qualifications/create_qualification.html', {'form': form})

# List Qualifications (for selecting qualification when assigning to teacher)


# @login_required
# def list_qualifications(request):
#     qualifications = Qualification.objects.all().order_by('name')
#     qualification_name = request.GET.get('qualification')
#     return render(request, 'qualifications/list_qualifications.html', {'qualifications': qualifications})

# Edit View


@login_required
def edit_qualification(request, pk):
    qualification = get_object_or_404(Qualification, pk=pk)
    if request.method == 'POST':
        form = QualificationForm(request.POST, instance=qualification)
        if form.is_valid():
            form.save()
            messages.success(request, 'Qualification updated successfully!')
            return redirect('list_qualifications')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = QualificationForm(instance=qualification)

    return render(request, 'qualifications/edit_qualification.html', {'form': form})

# Delete View


@login_required
def delete_qualification(request, pk):
    qualification = get_object_or_404(Qualification, pk=pk)
    if request.method == 'POST':
        qualification.delete()
        return redirect('list_qualifications')
    return redirect('list_qualifications')
