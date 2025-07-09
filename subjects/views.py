from django.shortcuts import render, get_object_or_404, redirect
from .models import Subject, TeacherSubject
from .forms import SubjectForm, TeacherSubjectFormSet
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator

# Check if the user is an admin


def is_admin(user):
    return user.role == 'admin'

# List all subjects


@login_required
@user_passes_test(is_admin)
def list_subject(request):
    subjects = Subject.objects.all().order_by('subject_name')

    # Pagination setup
    paginator = Paginator(subjects, 10)  # Show 10 students per page
    page_number = request.GET.get('page')
    subjects_page = paginator.get_page(page_number)

    return render(request, 'subjects/list_subject.html', {'subjects': subjects_page})

# Create a new subject


@login_required
@user_passes_test(is_admin)
def create_subject(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        formset = TeacherSubjectFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            subject = form.save()
            formset.instance = subject
            formset.save()
            return redirect('list_subject')
    else:
        form = SubjectForm()
        formset = TeacherSubjectFormSet()

    return render(request, 'subjects/form_subject.html', {'form': form, 'formset': formset})

# Edit an existing subject


@login_required
@user_passes_test(is_admin)
def edit_subject(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        formset = TeacherSubjectFormSet(request.POST, instance=subject)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('list_subject')
    else:
        form = SubjectForm(instance=subject)
        formset = TeacherSubjectFormSet(instance=subject)

    return render(request, 'subjects/form_subject.html', {'form': form, 'formset': formset})

# Delete a subject


@login_required
@user_passes_test(is_admin)
def delete_subject(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        subject.delete()
        return redirect('list_subject')
    return redirect('list_subject')

# View subject details


@login_required
@user_passes_test(is_admin)
def detail_subject(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    return render(request, 'subjects/detail_subject.html', {'subject': subject})


# def list_subject_teacher(request, subject_id):
#     subject = get_object_or_404(Subject, pk=subject_id)
#     teachers = Teacher.objects.all()  # List all teachers
#     teacher_subjects = TeacherSubject.objects.filter(subject=subject)

#     if request.method == 'POST':
#         form = TeacherSubjectForm(request.POST)
#         if form.is_valid():
#             # Create a new Teacher-Subject association
#             teacher_subject = form.save(commit=False)
#             teacher_subject.subject = subject
#             teacher_subject.save()
#             return redirect('list_subject_teacher', subject_id=subject.id)
#     else:
#         form = TeacherSubjectForm()

#     return render(request, 'subjects/list_subject_teacher.html', {
#         'subject': subject,
#         'teachers': teachers,
#         'teacher_subjects': teacher_subjects,
#         'form': form,
#     })
@login_required
@user_passes_test(is_admin)
def list_subject_teacher(request):
    subjects = TeacherSubject.objects.all()
    return render(request, 'subjects/list_subject_teacher.html', {'subjects': subjects})


@login_required
def delete_teacher_subject(request, pk):
    teacher_subject = get_object_or_404(TeacherSubject, pk=pk)
    subject_id = teacher_subject.subject.id
    teacher_subject.delete()
    return redirect('list_subject_teacher', subject_id=subject_id)
