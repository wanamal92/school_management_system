from django.shortcuts import render, redirect, get_object_or_404
from .models import Class
from .forms import ClassForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.contrib import messages

# Check if the user is an admin


def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

def is_admin_or_staff(user):
    return user.is_authenticated and user.role in ['admin', 'staff']

@login_required
@user_passes_test(is_admin_or_staff)
def list_class(request):
    classes = Class.objects.all().order_by('class_name')

    # Pagination setup
    paginator = Paginator(classes, 10)  # Show 10 students per page
    page_number = request.GET.get('page')
    classes_page = paginator.get_page(page_number)

    return render(request, 'clases/list_class.html', {'classes': classes_page})


@login_required
@user_passes_test(is_admin_or_staff)
def detail_class(request, pk):
    cls = get_object_or_404(Class, pk=pk)
    return render(request, 'clases/detail_class.html', {'cls': cls})


@login_required
@user_passes_test(is_admin)
def create_class(request):
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Class created successfully!")

            return redirect('list_class')
        else:
            messages.error(request, "There was an error in creating the class.")

    else:
        form = ClassForm()
    return render(request, 'clases/form_class.html', {'form': form})


@login_required
@user_passes_test(is_admin)
def edit_class(request, pk):
    cls = get_object_or_404(Class, pk=pk)
    if request.method == 'POST':
        form = ClassForm(request.POST, instance=cls)
        if form.is_valid():
            form.save()
            messages.success(request, "Class updated successfully!")

            return redirect('list_class')
        else:
            messages.error(request, "There was an error updating the class.")

    else:
        form = ClassForm(instance=cls)
    return render(request, 'clases/form_class.html', {'form': form})


@login_required
@user_passes_test(is_admin)
def delete_class(request, pk):
    cls = get_object_or_404(Class, pk=pk)
    if request.method == 'POST':
        cls.delete()
        messages.success(request, "Class deleted successfully!")

        return redirect('list_class')
    return redirect('list_class')
