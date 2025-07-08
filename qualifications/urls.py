# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('list_teacher_qualifictions', views.list_teacher_qualifications, name='list_teacher_qualifications'),
    path('create_teacher_qualifictions/', views.create_teacher_qualification, name='create_teacher_qualification'),
    path('edit_teacher_qualifictions/<int:pk>/', views.edit_teacher_qualification, name='edit_teacher_qualification'),
    path('delete_teacher_qualifictions/<int:pk>/', views.delete_teacher_qualification, name='delete_teacher_qualification'),

    path('list_qualifictions/', views.list_qualifications, name='list_qualifications'),
    path('create_qualification/', views.create_qualification, name='create_qualification'),
    path('edit_qualification/<int:pk>/', views.edit_qualification, name='edit_qualification'),
    path('delete_qualification/<int:pk>/', views.delete_qualification, name='delete_qualification'),
]
