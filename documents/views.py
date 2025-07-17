from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, FileResponse,  Http404
from .models import Document
from .forms import DocumentForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
import os
from django.core.paginator import Paginator
from django.conf import settings

# Create Document
def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

def is_admin_or_staff(user):
    return user.is_authenticated and user.role in ['admin', 'staff']

@user_passes_test(is_admin)
@login_required
def create_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Document created successfully!')
            return redirect('list_documents')  # Adjust URL name as needed
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = DocumentForm()

    return render(request, 'documents/create_document.html', {'form': form})

# List Documents (with filtering and searching)

@user_passes_test(is_admin)
@login_required
def list_documents(request):
    documents = Document.objects.all().order_by('document_type')

    teacher_name = request.GET.get('teacher')
    student_name = request.GET.get('student')
    document_type = request.GET.get('document_type')
    user_type = request.GET.get('user_type')

    if teacher_name:
        documents = documents.filter(
            teacher__full_name__icontains=teacher_name)
    if student_name:
        documents = documents.filter(
            student__full_name__icontains=student_name)
    if document_type:
        documents = documents.filter(document_type=document_type)
    if user_type:
        documents = documents.filter(user_type=user_type)

    # Pagination setup
    paginator = Paginator(documents, 10)  # Show 10 students per page
    page_number = request.GET.get('page')
    documents_page = paginator.get_page(page_number)

    return render(request, 'documents/list_documents.html', {'documents': documents_page})

# Edit Document

@user_passes_test(is_admin)
@login_required
def edit_document(request, pk):
    document = get_object_or_404(Document, pk=pk)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()
            messages.success(request, "Document updated successfully!")
            return redirect('list_documents')
        else:
            messages.error(request, "There was an error updating the document.")
    else:
        form = DocumentForm(instance=document)
    return render(request, 'documents/edit_document.html', {'form': form, 'document': document})

# Delete Document

@user_passes_test(is_admin)
@login_required
def delete_document(request, pk):
    document = get_object_or_404(Document, pk=pk)
    if request.method == 'POST':
        document.delete()
        messages.success(request, "Document deleted successfully!")
        return redirect('list_documents')
    return redirect('list_documents')

@user_passes_test(is_admin)
@login_required
def download_document(request, pk):
    # Get the document object using the primary key (pk)
    document = get_object_or_404(Document, pk=pk)

    # Get the file path of the document
    file_path = document.document_file.path
    print(f"Trying to download the file from: {file_path}")  # Log the file path for debugging

    # Check if the file exists
    if os.path.exists(file_path):
        try:
            file_extension = os.path.splitext(file_path)[1]
            # Generate the custom filename
            if document.teacher:
                filename = f"{document.teacher.full_name}_{document.document_type}{file_extension}"
            elif document.student:
                filename = f"{document.student.full_name}_{document.document_type}{file_extension}"
            else:
                filename = f"{document.document_type}{file_extension}"

            # Use 'open()' properly for FileResponse to handle it
            response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=filename)
            return response
        except Exception as e:
            print(f"Error opening file: {e}")  # Log the error message
            raise Http404(f"Error opening file: {e}")
    else:
        print(f"File not found at: {file_path}")  # Log file not found message
        raise Http404("File not found.")