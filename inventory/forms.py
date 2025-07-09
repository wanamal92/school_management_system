from django import forms
from .models import Item, Category, TeacherItem
from teachers.models import Teacher


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

# Form to create/update Item


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'category', 'quantity',
                  'status', 'price', 'description', 'added_date']

        widgets = {
            'added_date': forms.DateInput(attrs={'type': 'date'}),
        }


# Form to create/update TeacherItem (assign items to teachers)
class TeacherItemForm(forms.ModelForm):
    class Meta:
        model = TeacherItem
        fields = ['teacher', 'item', 'quantity', 'assigned_date']

        widgets = {
            'assigned_date': forms.DateInput(attrs={'type': 'date'}),
        }
