# exams/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import ExamSession, Exam, ExamAttendee
from .forms import ExamSessionForm, ExamForm, ExamAttendeeForm

# Exam sessions
def list_exam_session(request):
    exam_sessions = ExamSession.objects.all()
    return render(request, 'exams/list_exam_session.html', {'exam_sessions': exam_sessions})

def create_exam_session(request):
    if request.method == 'POST':
        form = ExamSessionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_exam_session')
    else:
        form = ExamSessionForm()
    return render(request, 'exams/create_exam_session.html', {'form': form})

def edit_exam_session(request, pk):
    exam_session = get_object_or_404(ExamSession, pk=pk)
    if request.method == 'POST':
        form = ExamSessionForm(request.POST, instance=exam_session)
        if form.is_valid():
            form.save()
            return redirect('list_exam_session')
    else:
        form = ExamSessionForm(instance=exam_session)
    return render(request, 'exams/create_exam_session.html', {'form': form})

def delete_exam_session(request, pk):
    exam_session = get_object_or_404(ExamSession, pk=pk)
    if request.method == 'POST':
        exam_session.delete()
        return redirect('list_exam_session')
    return render(request, 'exams/delete_exam_session.html', {'exam_session': exam_session})

def detail_exam_session(request, pk):
    exam_session = get_object_or_404(ExamSession, pk=pk)
    return render(request, 'exams/detail_exam_session.html', {'exam_session': exam_session})


# Exams 
def list_exam(request):
    exams = Exam.objects.all()
    return render(request, 'exams/list_exam.html', {'exams': exams})

def create_exam(request):
    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_exam')
    else:
        form = ExamForm()
    return render(request, 'exams/create_exam.html', {'form': form})

def edit_exam(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    if request.method == 'POST':
        form = ExamForm(request.POST, instance=exam)
        if form.is_valid():
            form.save()
            return redirect('list_exam')
    else:
        form = ExamForm(instance=exam)
    return render(request, 'exams/create_exam.html', {'form': form})

def delete_exam(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    if request.method == 'POST':
        exam.delete()
        return redirect('list_exam')
    return render(request, 'exams/delete_exam.html', {'exam': exam})

def detail_exam(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    return render(request, 'exams/detail_exam.html', {'exam': exam})



# Exam Attendees 
def list_exam_attendee(request):
    exam_attendees = ExamAttendee.objects.all()
    return render(request, 'exams/list_exam_attendee.html', {'exam_attendees': exam_attendees})

def create_exam_attendee(request):
    if request.method == 'POST':
        form = ExamAttendeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_exam_attendee')
    else:
        form = ExamAttendeeForm()
    return render(request, 'exams/create_exam_attendee.html', {'form': form})

def edit_exam_attendee(request, pk):
    exam_attendee = get_object_or_404(ExamAttendee, pk=pk)
    if request.method == 'POST':
        form = ExamAttendeeForm(request.POST, instance=exam_attendee)
        if form.is_valid():
            form.save()
            return redirect('list_exam_attendee')
    else:
        form = ExamAttendeeForm(instance=exam_attendee)
    return render(request, 'exams/create_exam_attendee.html', {'form': form})

def delete_exam_attendee(request, pk):
    exam_attendee = get_object_or_404(ExamAttendee, pk=pk)
    if request.method == 'POST':
        exam_attendee.delete()
        return redirect('list_exam_attendee')
    return render(request, 'exams/delete_exam_attendee.html', {'exam_attendee': exam_attendee})

def detail_exam_attendee(request, pk):
    exam_attendee = get_object_or_404(ExamAttendee, pk=pk)

    return render(request, 'exams/detail_exam_attendee.html', {'exam_attendee': exam_attendee})

