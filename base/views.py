from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from students.models import Student
from teachers.models import Teacher
from clases.models import Class
from exams.models import ExamSession
from subjects.models import Subject
from health.models import HealthRecord
from leaves.models import LeaveRequest
from guardians.models import Guardian


@login_required
def dashboard(request):
    if request.user.role == 'admin':
        students = Student.objects.all().count()
        teachers = Teacher.objects.all().count()
        classes = Class.objects.all().count()
        exams = ExamSession.objects.all().count()
        subjects = Subject.objects.all().count()
        health_records = HealthRecord.objects.all().count()
        leaves = LeaveRequest.objects.filter(status='Pending').count()
        guardians = Guardian.objects.all().count()
        context = {
            'students': students,
            'teachers': teachers,
            'classes': classes,
            'exams': exams,
            'subjects': subjects,
            'health_records': health_records,
            'leaves': leaves,
            'guardians': guardians,
        }
        return render(request, 'dashboards/admin.html', context)
    elif request.user.role == 'staff':
        return render(request, 'dashboards/staff.html')
    elif request.user.role == 'guardian':
        return render(request, 'dashboards/guardian.html')
    elif request.user.role == 'student':
        return render(request, 'dashboards/student.html')
    else:
        return redirect('login')
