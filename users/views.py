from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
from django.contrib.auth.forms import SetPasswordForm

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if user.must_change_password:
                return redirect('force_password_change')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'users/login.html')


def user_logout(request):
    logout(request)
    return redirect('login')


def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

@login_required
@user_passes_test(is_admin)
def user_list(request):
    users = CustomUser.objects.all()
    return render(request, 'users/user_list.html', {'users': users})

@login_required
@user_passes_test(is_admin)
def user_create(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/user_form.html', {'form': form, 'title': 'Add User'})

@login_required
@user_passes_test(is_admin)
def user_edit(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = CustomUserChangeForm(instance=user)
    return render(request, 'users/user_form.html', {'form': form, 'title': 'Edit User'})

@login_required
@user_passes_test(is_admin)
def user_delete(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.delete()
    return redirect('user_list')

@login_required
def dashboard(request):
    if request.user.role == 'admin':
        return render(request, 'dashboards/admin.html')
    elif request.user.role == 'staff':
        return render(request, 'dashboards/staff.html')
    elif request.user.role == 'guardian':
        return render(request, 'dashboards/guardian.html')
    elif request.user.role == 'student':
        return render(request, 'dashboards/student.html')
    else:
        return redirect('login')


@login_required
def profile_view(request):
    return render(request, 'users/profile_view.html')

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

@login_required
def profile_edit(request):
    if request.method == 'POST':
        image = request.FILES.get('profile_image')
        if image:
            request.user.profile_image = image
            request.user.save()

        password_form = PasswordChangeForm(user=request.user, data=request.POST)
        if password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request, request.user)  # Keep user logged in
            return redirect('profile_view')
    else:
        password_form = PasswordChangeForm(user=request.user)
    return render(request, 'users/profile_edit.html', {
        'password_form': password_form,
        'user_profile_image': request.user.profile_image
    })


@login_required
def force_password_change(request):
    if not request.user.must_change_password:
        return redirect('dashboard')

    if request.method == 'POST':
        form = SetPasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            request.user.must_change_password = False
            request.user.save()
            update_session_auth_hash(request, request.user)
            return redirect('dashboard')
    else:
        form = SetPasswordForm(request.user)
    return render(request, 'users/force_password_change.html', {'form': form})

