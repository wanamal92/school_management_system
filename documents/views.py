from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, FileResponse,  Http404
from .models import Document
from .forms import DocumentForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import os

# Create Document
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
@login_required
def list_documents(request):
    documents = Document.objects.all()
    
    teacher_name = request.GET.get('teacher')
    student_name = request.GET.get('student')
    document_type = request.GET.get('document_type')
    user_type = request.GET.get('user_type')
    
    if teacher_name:
        documents = documents.filter(teacher__full_name__icontains=teacher_name)
    if student_name:
        documents = documents.filter(student__full_name__icontains=student_name)
    if document_type:
        documents = documents.filter(document_type=document_type)
    if user_type:
        documents = documents.filter(user_type=user_type)
    
    return render(request, 'documents/list_documents.html', {'documents': documents})

# Edit Document
@login_required
def edit_document(request, pk):
    document = get_object_or_404(Document, pk=pk)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()
            return redirect('list_documents')
    else:
        form = DocumentForm(instance=document)
    return render(request, 'documents/edit_document.html', {'form': form, 'document': document})

# Delete Document
@login_required

@login_required
def delete_document(request, pk):
    document = get_object_or_404(Document, pk=pk)
    if request.method == 'POST':
        document.delete()
        return redirect('list_documents')
    return render(request, 'documents/delete_document.html', {'document': document})




def download_document(request, pk):
    # Get the document object using the primary key (pk)
    document = get_object_or_404(Document, pk=pk)

    # Get the file path of the document
    file_path = document.document_file.path

    # Check if the file exists
    if os.path.exists(file_path):
        try:
            # Return the file as a response for download
                        # Generate the custom filename
            if document.teacher:
                filename = f"{document.teacher.full_name}_{document.document_type}.pdf"  # Example format
            elif document.student:
                filename = f"{document.student.full_name}_{document.document_type}.pdf"  # Example format
            else:
                filename = f"{document.document_type}.pdf" 
            return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=filename)
        except Exception as e:
            print(f"Error opening file: {e}")
            raise Http404("File cannot be opened.")
    else:
        raise Http404("File not found.")