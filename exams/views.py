# exams/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import ExamSession, Exam, ExamAttendee
from .forms import ExamSessionForm, ExamForm, ExamAttendeeForm, ExcelUploadForm
import pandas as pd
from clases.models import Class
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from zipfile import BadZipFile

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

def upload_exam_session_excel(request):
    if request.method == 'POST' and request.FILES['excel_file']:
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Get the uploaded Excel file
            excel_file = request.FILES['excel_file']
            
            # Check if the file is a valid Excel file (by trying to read it)
            try:
                # Try reading the Excel file (forcing pandas to use the right engine for .xlsx)
                df = pd.read_excel(excel_file, engine='openpyxl')  # Specify engine for .xlsx files
                
            except BadZipFile:
                # Handle the error for invalid Excel files (not a valid ZIP/Excel file)
                return render(request, 'exams/upload_exam_session_excel.html', {
                    'form': form,
                    'error': 'Error: The uploaded file is not a valid Excel file. Please upload a valid Excel file.'
                })

            except ValueError as e:
                # If pandas cannot read the file, show a friendly error
                return render(request, 'exams/upload_exam_session_excel.html', {
                    'form': form,
                    'error': 'Error: Invalid file format. Please upload a valid Excel file.'
                })

            # Proceed with the rest of the file processing (create records, etc.)
            for index, row in df.iterrows():
                # Fetch the Class instance based on the class name (e.g., 'Grade 1')
                try:
                    class_assigned = Class.objects.get(class_name=row['class_assigned'])
                except Class.DoesNotExist:
                    class_assigned = None  # Handle case where class doesn't exist

                # Check if exam_session_code already exists
                if ExamSession.objects.filter(exam_session_code=row['exam_session_code']).exists():
                    # Return error if the session code already exists
                    return render(request, 'exams/upload_exam_session_excel.html', {
                        'form': form, 
                        'error': f"Error: Exam session code '{row['exam_session_code']}' already exists!"
                    })

                try:
                    # Create ExamSession if no error
                    ExamSession.objects.create(
                        exam_session_name=row['exam_session_name'],
                        exam_session_code=row['exam_session_code'],
                        start_date=row['start_date'],
                        end_date=row['end_date'],
                        exam_type=row['exam_type'],
                        academic_year=row['academic_year'],
                        class_assigned=class_assigned,
                    )
                except IntegrityError:
                    return render(request, 'exams/upload_exam_session_excel.html', {
                        'form': form,
                        'error': f"Error: Integrity error occurred for row {index + 1}. Please check your data."
                    })
            
            return redirect('list_exam_sessions')  # Redirect after successful upload
    else:
        form = ExcelUploadForm()

    return render(request, 'exams/upload_exam_session_excel.html', {'form': form})