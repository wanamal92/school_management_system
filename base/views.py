from django.shortcuts import render
from django.contrib.auth.decorators import login_required

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
