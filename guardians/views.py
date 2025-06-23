from django.shortcuts import render, redirect, get_object_or_404
from .models import Guardian
from .forms import GuardianForm
from django.contrib.auth.decorators import login_required, user_passes_test


def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

# List all guardians
@user_passes_test(is_admin)
@login_required
def list_guardian(request):
    # Get the view mode from the URL parameter (default is 'list')
    view_mode = request.GET.get('view', 'list')
    
    # Fetch all the guardians (you can modify this query based on your needs)
    guardians = Guardian.objects.all()
    
    # Pass the guardians and view_mode to the template
    return render(request, 'guardians/list_guardian.html', {
        'guardians': guardians,
        'view_mode': view_mode,
    })

# Add a new guardian
@user_passes_test(is_admin)
@login_required
def add_guardian(request):
    if request.method == 'POST':
        form = GuardianForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('list_guardian')
    else:
        form = GuardianForm()
    return render(request, 'guardians/add_guardian.html', {'form': form})

# Edit an existing guardian
@user_passes_test(is_admin)
@login_required
def edit_guardian(request, pk):
    guardian = get_object_or_404(Guardian, pk=pk)
    if request.method == 'POST':
        form = GuardianForm(request.POST, instance=guardian)
        if form.is_valid():
            form.save()
            return redirect('list_guardian')
    else:
        form = GuardianForm(instance=guardian)
    return render(request, 'guardians/edit_guardian.html', {'form': form})

# Delete a guardian
@user_passes_test(is_admin)
@login_required
def delete_guardian(request, pk):
    guardian = get_object_or_404(Guardian, pk=pk)
    if request.method == 'POST':
        guardian.delete()
        return redirect('list_guardian')
    return render(request, 'guardians/delete_guardian.html', {'guardian': guardian})

@user_passes_test(is_admin)
@login_required
def detail_guardian(request, pk):
    guardian = get_object_or_404(Guardian, pk=pk)
    return render(request, 'guardians/detail_guardian.html', {'guardian': guardian})


@login_required
def profile_guardian(request):
    # Fetch the guardian's profile related to the logged-in user
    try:
        guardian_profile = Guardian.objects.get(user=request.user)
    except Guardian.DoesNotExist:
        guardian_profile = None  # or handle if the profile does not exist

    return render(request, 'guardians/profile_guardian.html', {'guardian_profile': guardian_profile})