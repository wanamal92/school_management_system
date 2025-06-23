from django.shortcuts import render, redirect, get_object_or_404
from .models import Class
from .forms import ClassForm
from django.contrib.auth.decorators import login_required, user_passes_test

# Check if the user is an admin
def is_admin(user):
    return user.role == 'admin'

@login_required
@user_passes_test(is_admin)
def list_class(request):
    classes = Class.objects.all()
    return render(request, 'classes/list_class.html', {'classes': classes})

@login_required
@user_passes_test(is_admin)
def detail_class(request, pk):
    cls = get_object_or_404(Class, pk=pk)
    return render(request, 'classes/detail_class.html', {'cls': cls})

@login_required
@user_passes_test(is_admin)
def create_class(request):
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_class')
    else:
        form = ClassForm()
    return render(request, 'classes/form_class.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def edit_class(request, pk):
    cls = get_object_or_404(Class, pk=pk)
    if request.method == 'POST':
        form = ClassForm(request.POST, instance=cls)
        if form.is_valid():
            form.save()
            return redirect('list_class')
    else:
        form = ClassForm(instance=cls)
    return render(request, 'classes/form_class.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def delete_class(request, pk):
    cls = get_object_or_404(Class, pk=pk)
    if request.method == 'POST':
        cls.delete()
        return redirect('list_class')
    return render(request, 'classes/confirm_delete_class.html', {'cls': cls})
