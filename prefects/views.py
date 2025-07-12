from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Prefect
from .forms import PrefectForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator

def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

def is_admin_or_staff(user):
    return user.is_authenticated and user.role in ['admin', 'staff']

@login_required
@user_passes_test(is_admin_or_staff)
def list_prefects(request):
    prefects = Prefect.objects.all().order_by('student__full_name')
    
    # Pagination setup
    paginator = Paginator(prefects, 10)  # Show 10 students per page
    page_number = request.GET.get('page')
    prefects_page = paginator.get_page(page_number)

    return render(request, 'prefects/list_prefects.html', {'prefects': prefects_page})

@login_required
@user_passes_test(is_admin_or_staff)
def create_prefect(request):
    if request.method == 'POST':
        form = PrefectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Prefect created successfully!")
            return redirect('list_prefects')
        else:
            messages.error(request, "There was an error in creating the prefect.")
    else:
        form = PrefectForm()

    return render(request, 'prefects/create_prefect.html', {'form': form})

@login_required
@user_passes_test(is_admin_or_staff)
def edit_prefect(request, pk):
    prefect = get_object_or_404(Prefect, pk=pk)
    if request.method == 'POST':
        form = PrefectForm(request.POST, instance=prefect)
        if form.is_valid():
            form.save()
            messages.success(request, "Prefect updated successfully!")
            return redirect('list_prefects')
        else:
            messages.error(request, "There was an error updating the prefect.")
    else:
        form = PrefectForm(instance=prefect)

    return render(request, 'prefects/edit_prefect.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def delete_prefect(request, pk):
    prefect = get_object_or_404(Prefect, pk=pk)
    if request.method == 'POST':
        prefect.delete()
        messages.success(request, "Prefect deleted successfully!")
        return redirect('list_prefects')
    return redirect('list_prefects')
