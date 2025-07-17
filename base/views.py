from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from students.models import Student
from teachers.models import Teacher
from clases.models import Class
from exams.models import ExamSession
from subjects.models import Subject
from health.models import HealthRecord
from leaves.models import LeaveRequest
from guardians.models import Guardian
from sections.models import Section


@login_required
def dashboard(request):
    my_leaves= None
    my_childrens = None
    classes = Class.objects.all().count()
    sections = Section.objects.all().count()
    students = Student.objects.all().count()
    
    teachers = Teacher.objects.all().count()
    exams = ExamSession.objects.all().count()
    subjects = Subject.objects.all().count()
    health_records = HealthRecord.objects.all().count()
    leaves = LeaveRequest.objects.filter(status='Pending').count()
    guardians = Guardian.objects.all().count()
    if request.user.role == "staff":
        
        logged_in_teacher = Teacher.objects.get(user=request.user)        
        my_leaves = LeaveRequest.objects.filter(
        status='Pending', teacher=logged_in_teacher).count()

    if request.user.role == "guardian":    
        logged_in_guardian = Guardian.objects.get(user=request.user)
        my_childrens = Student.objects.filter(guardian=logged_in_guardian).count()

    context = {
        'students': students,
        'teachers': teachers,
        'classes': classes,
        'exams': exams,
        'subjects': subjects,
        'health_records': health_records,
        'leaves': leaves,
        'guardians': guardians,
        'sections': sections,
        'my_childrens': my_childrens,
        'my_leaves': my_leaves,
    }
    if request.user.role == 'admin':

        return render(request, 'dashboards/admin.html', context)
    elif request.user.role == 'staff':
        return render(request, 'dashboards/staff.html', context)
    elif request.user.role == 'guardian':
        return render(request, 'dashboards/guardian.html', context)
    elif request.user.role == 'student':
        return render(request, 'dashboards/student.html', context)
    else:
        return redirect('login')
