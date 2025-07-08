from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Competition, CompetitionResult
from .forms import CompetitionForm, CompetitionResultForm

# View to list all competitions
def list_competitions(request):
    competitions = Competition.objects.all()
    return render(request, 'competitions/list_competitions.html', {'competitions': competitions})

# View to create a new competition
def create_competition(request):
    if request.method == 'POST':
        form = CompetitionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Competition created successfully.")
            return redirect('list_competitions')
    else:
        form = CompetitionForm()
    return render(request, 'competitions/create_competition.html', {'form': form})

# View to update an existing competition
def edit_competition(request, pk):
    competition = get_object_or_404(Competition, pk=pk)
    if request.method == 'POST':
        form = CompetitionForm(request.POST, instance=competition)
        if form.is_valid():
            form.save()
            messages.success(request, "Competition updated successfully.")
            return redirect('list_competitions')
    else:
        form = CompetitionForm(instance=competition)
    return render(request, 'competitions/edit_competition.html', {'form': form})

# View to delete a competition
def delete_competition(request, pk):
    competition = get_object_or_404(Competition, pk=pk)
    competition.delete()
    messages.success(request, "Competition deleted successfully.")
    return redirect('list_competitions')

# View to list all competition results
def list_competition_results(request):
    results = CompetitionResult.objects.all()
    return render(request, 'competitions/list_competition_results.html', {'results': results})

# View to create a new competition result
def create_competition_result(request):
    if request.method == 'POST':
        form = CompetitionResultForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Competition result added successfully.")
            return redirect('list_competition_results')
    else:
        form = CompetitionResultForm()
    return render(request, 'competitions/create_competition_result.html', {'form': form})

# View to edit an existing competition result
def edit_competition_result(request, pk):
    result = get_object_or_404(CompetitionResult, pk=pk)
    if request.method == 'POST':
        form = CompetitionResultForm(request.POST, instance=result)
        if form.is_valid():
            form.save()
            messages.success(request, "Competition result updated successfully.")
            return redirect('list_competition_results')
    else:
        form = CompetitionResultForm(instance=result)
    return render(request, 'competitions/edit_competition_result.html', {'form': form})

# View to delete a competition result
def delete_competition_result(request, pk):
    result = get_object_or_404(CompetitionResult, pk=pk)
    result.delete()
    messages.success(request, "Competition result deleted successfully.")
    return redirect('list_competition_results')
