from django.urls import path
from . import views


urlpatterns = [
    path('', views.list_duties, name='list_duties'),
    path('create/', views.create_duty, name='create_duty'),
    path('edit/<int:pk>/', views.edit_duty, name='edit_duty'),
    path('delete/<int:pk>/', views.delete_duty, name='delete_duty'),
    
    path('teacher-duties/', views.list_teacher_duties, name='list_teacher_duties'),
    path('teacher-duties/create/', views.create_teacher_duty, name='create_teacher_duty'),
    path('teacher-duties/edit/<int:pk>/', views.edit_teacher_duty, name='edit_teacher_duty'),
    path('teacher-duties/delete/<int:pk>/', views.delete_teacher_duty, name='delete_teacher_duty'),
]
