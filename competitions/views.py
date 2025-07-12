from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Competition, CompetitionResult
from .forms import CompetitionForm, CompetitionResultForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, user_passes_test

# View to list all competitions

def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

def is_admin_or_staff(user):
    return user.is_authenticated and user.role in ['admin', 'staff']

@user_passes_test(is_admin_or_staff)
@login_required
def list_competitions(request):
    competitions = Competition.objects.all().order_by('name')
    # Pagination setup
    paginator = Paginator(competitions, 10)  # Show 10 students per page
    page_number = request.GET.get('page')
    competitions_page = paginator.get_page(page_number)
    return render(request, 'competitions/list_competitions.html', {'competitions': competitions_page})

# View to create a new competition

@user_passes_test(is_admin_or_staff)
@login_required
def create_competition(request):
    if request.method == 'POST':
        form = CompetitionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Competition created successfully.")
            return redirect('list_competitions')
        else:
            messages.error(request, "There was an error in creating the competition.")
    else:
        form = CompetitionForm()
    return render(request, 'competitions/create_competition.html', {'form': form})

# View to update an existing competition

@user_passes_test(is_admin_or_staff)
@login_required
def edit_competition(request, pk):
    competition = get_object_or_404(Competition, pk=pk)
    if request.method == 'POST':
        form = CompetitionForm(request.POST, instance=competition)
        if form.is_valid():
            form.save()
            messages.success(request, "Competition updated successfully.")
            return redirect('list_competitions')
        else:
            messages.error(request, "There was an error updating the competition.")
    else:
        form = CompetitionForm(instance=competition)
    return render(request, 'competitions/edit_competition.html', {'form': form})

# View to delete a competition

@user_passes_test(is_admin)
@login_required
def delete_competition(request, pk):
    competition = get_object_or_404(Competition, pk=pk)
    if request.method == 'POST':
        competition.delete()
        messages.success(request, "Competition deleted successfully.")
        return redirect('list_competitions')
    return redirect('list_competitions')


# View to list all competition results
@user_passes_test(is_admin_or_staff)
@login_required
def list_competition_results(request):
    results = CompetitionResult.objects.all().order_by('student__full_name')
    # Pagination setup
    paginator = Paginator(results, 10)  # Show 10 students per page
    page_number = request.GET.get('page')
    results_page = paginator.get_page(page_number)
    return render(request, 'competitions/list_competition_results.html', {'results': results_page})

# View to create a new competition result

@user_passes_test(is_admin_or_staff)
@login_required
def create_competition_result(request):
    if request.method == 'POST':
        form = CompetitionResultForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Competition result added successfully.")
            return redirect('list_competition_results')
        else:
            messages.error(request, "There was an error in creating the competition result.")
    else:
        form = CompetitionResultForm()
    return render(request, 'competitions/create_competition_result.html', {'form': form})

# View to edit an existing competition result

@user_passes_test(is_admin_or_staff)
@login_required
def edit_competition_result(request, pk):
    result = get_object_or_404(CompetitionResult, pk=pk)
    if request.method == 'POST':
        form = CompetitionResultForm(request.POST, instance=result)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Competition result updated successfully.")
            return redirect('list_competition_results')
        else:
            messages.error(request, "There was an error updating the competition result.")
    else:
        form = CompetitionResultForm(instance=result)
    return render(request, 'competitions/edit_competition_result.html', {'form': form})

# View to delete a competition result

@user_passes_test(is_admin)
@login_required
def delete_competition_result(request, pk):
    result = get_object_or_404(CompetitionResult, pk=pk)
    if request.method == 'POST':
        result.delete()
        messages.success(request, "Competition result deleted successfully.")
        return redirect('list_competition_results')
    return redirect('list_competition_results')
