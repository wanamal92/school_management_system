from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
from django.contrib.auth.forms import SetPasswordForm
from .models import AuditLog
from axes.handlers.proxy import AxesProxyHandler
from axes.utils import reset


from django.contrib import messages

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        axes_handler = AxesProxyHandler()

        if user:
            if user.is_active:
                login(request, user)
                if user.must_change_password:
                    return redirect('force_password_change')
                return redirect('dashboard')
            else:
                messages.error(request, 'Your account has been deactivated. Please contact admin.')
        else:
            # ✅ Use proxy handler with request + credentials
            is_locked = axes_handler.is_locked(request=request, credentials={'username': username})
            if is_locked:
                messages.error(request, 'Too many failed attempts. Account locked. Try again later.')
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
    axes_handler = AxesProxyHandler()

    for user in users:
        user.is_locked = axes_handler.is_locked(request=request, credentials={'username': user.username})

    return render(request, 'users/user_list.html', {'users': users})

@login_required
@user_passes_test(is_admin)
def user_detail(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    return render(request, 'users/user_detail.html', {'user': user})


@login_required
@user_passes_test(is_admin)
def user_create(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password('TempPass123')  # or generate random password
            user.must_change_password = True
            user.save()

            # 🔍 Create audit log
            AuditLog.objects.create(
                performed_by=request.user,
                target_user=user,
                action='create'
            )

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

    if user == request.user:
        messages.error(request, "You cannot delete your own account.")
        return redirect('user_list')

    # 🔍 Log before deletion
    AuditLog.objects.create(
        performed_by=request.user,
        target_user=user,
        action='delete'
    )

    user.delete()
    messages.success(request, "User deleted.")
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
        print(f"Form data: {request.POST}")
        print(f"Form is valid: {form.is_valid()}")
        print(f"Form Errors: {form.errors}")
        
        if form.is_valid():
            print("Form is valid")
            form.save()
            request.user.must_change_password = False
            request.user.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, "Your password has been successfully updated.")
            return redirect('dashboard')
        else:
            
            messages.error(request, f"Error: {form.errors}")  # Display errors on the UI
    else:
        form = SetPasswordForm(request.user)

    return render(request, 'users/force_password_change.html', {'form': form})


from django.contrib import messages



@login_required
@user_passes_test(is_admin)
def toggle_user_status(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if user == request.user:
        messages.error(request, "You cannot deactivate your own account.")
        return redirect('user_list')

    user.is_active = not user.is_active
    user.save()

    # Create log entry
    AuditLog.objects.create(
        performed_by=request.user,
        target_user=user,
        action='reactivate' if user.is_active else 'deactivate'
    )

    status = "activated" if user.is_active else "deactivated"
    messages.success(request, f"{user.username} has been {status}.")
    return redirect('user_list')

@login_required
@user_passes_test(is_admin)
def audit_log_list(request):
    logs = AuditLog.objects.select_related('performed_by', 'target_user').order_by('-timestamp')
    return render(request, 'users/audit_log_list.html', {'logs': logs})



@login_required
@user_passes_test(is_admin)
def unlock_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    axes_handler = AxesProxyHandler()

    if not axes_handler.is_locked(request=request, credentials={'username': user.username}):
        messages.info(request, f"{user.username} is not currently locked.")
        return redirect('user_list')


    reset(username=user.username)
    messages.success(request, f"{user.username} has been unlocked.")
    return redirect('user_list')
