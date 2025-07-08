from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Category, Item, TeacherItem
from .forms import CategoryForm,ItemForm, TeacherItemForm

# Category Views
def list_categories(request):
    categories = Category.objects.all()
    return render(request, 'inventory/list_categories.html', {'categories': categories})

def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category created successfully.")
            return redirect('list_categories')
    else:
        form = CategoryForm()
    return render(request, 'inventory/create_category.html', {'form': form})

def edit_category(request, pk):
    category = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category updated successfully.")
            return redirect('list_categories')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'inventory/edit_category.html', {'form': form})

def delete_category(request, pk):
    category = get_object_or_404(Item, pk=pk)
    category.delete()
    messages.success(request, "category deleted successfully.")
    return redirect('list_categories')

# Item Views
def list_items(request):
    items = Item.objects.all()
    return render(request, 'inventory/list_items.html', {'items': items})

def create_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Item created successfully.")
            return redirect('list_items')
    else:
        form = ItemForm()
    return render(request, 'inventory/create_item.html', {'form': form})

def edit_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Item updated successfully.")
            return redirect('list_items')
    else:
        form = ItemForm(instance=item)
    return render(request, 'inventory/edit_item.html', {'form': form})

def delete_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    item.delete()
    messages.success(request, "Item deleted successfully.")
    return redirect('list_items')

# Teacher Item Views (assign items to teachers)
def list_teacher_items(request):
    teacher_items = TeacherItem.objects.all()
    return render(request, 'inventory/list_teacher_items.html', {'teacher_items': teacher_items})

def create_teacher_item(request):
    if request.method == 'POST':
        form = TeacherItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Item assigned to teacher successfully.")
            return redirect('list_teacher_items')
    else:
        form = TeacherItemForm()
    return render(request, 'inventory/create_teacher_item.html', {'form': form})

def edit_teacher_item(request, pk):
    teacher_item = get_object_or_404(TeacherItem, pk=pk)
    if request.method == 'POST':
        form = TeacherItemForm(request.POST, instance=teacher_item)
        if form.is_valid():
            form.save()
            messages.success(request, "Teacher item updated successfully.")
            return redirect('list_teacher_items')
    else:
        form = TeacherItemForm(instance=teacher_item)
    return render(request, 'inventory/edit_teacher_item.html', {'form': form})

def delete_teacher_item(request, pk):
    teacher_item = get_object_or_404(TeacherItem, pk=pk)
    teacher_item.delete()
    messages.success(request, "Teacher item deleted successfully.")
    return redirect('list_teacher_items')
