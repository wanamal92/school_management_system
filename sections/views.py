from django.shortcuts import render, redirect, get_object_or_404
from .models import Section
from .forms import SectionForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator

# Check if the user is an admin


def is_admin(user):
    return user.role == 'admin'


@login_required
@user_passes_test(is_admin)
def list_section(request):
    sections = Section.objects.all().order_by('section_name')

    # Pagination setup
    paginator = Paginator(sections, 10)  # Show 10 students per page
    page_number = request.GET.get('page')
    sections_page = paginator.get_page(page_number)

    return render(request, 'sections/list_section.html', {'sections': sections_page})


@login_required
@user_passes_test(is_admin)
def detail_section(request, pk):
    cls = get_object_or_404(Section, pk=pk)
    return render(request, 'sections/detail_section.html', {'cls': cls})


@login_required
@user_passes_test(is_admin)
def create_section(request):
    if request.method == 'POST':
        form = SectionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_section')
    else:
        form = SectionForm()
    return render(request, 'sections/form_section.html', {'form': form})


@login_required
@user_passes_test(is_admin)
def edit_section(request, pk):
    cls = get_object_or_404(Section, pk=pk)
    if request.method == 'POST':
        form = SectionForm(request.POST, instance=cls)
        if form.is_valid():
            form.save()
            return redirect('list_section')
    else:
        form = SectionForm(instance=cls)
    return render(request, 'sections/form_section.html', {'form': form})


@login_required
@user_passes_test(is_admin)
def delete_section(request, pk):
    cls = get_object_or_404(Section, pk=pk)
    if request.method == 'POST':
        cls.delete()
        return redirect('list_section')
    return redirect('list_section')
