from django.urls import path
from . import views


urlpatterns = [
    # Category URLs
    path('categories/', views.list_categories, name='list_categories'),
    path('categories/create/', views.create_category, name='create_category'),
    path('categories/edit/<int:pk>/', views.edit_category, name='edit_category'),
    path('categories/delete/<int:pk>/',
         views.delete_category, name='delete_category'),

    # Item URLs
    path('items/', views.list_items, name='list_items'),
    path('items/create/', views.create_item, name='create_item'),
    path('items/edit/<int:pk>/', views.edit_item, name='edit_item'),
    path('items/delete/<int:pk>/', views.delete_item, name='delete_item'),

    # Teacher Item URLs
    path('teacher-items/', views.list_teacher_items, name='list_teacher_items'),
    path('teacher-items/create/', views.create_teacher_item,
         name='create_teacher_item'),
    path('teacher-items/edit/<int:pk>/',
         views.edit_teacher_item, name='edit_teacher_item'),
    path('teacher-items/delete/<int:pk>/',
         views.delete_teacher_item, name='delete_teacher_item'),

]
