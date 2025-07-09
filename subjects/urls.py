from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_subject, name='list_subject'),
    path('create/', views.create_subject, name='create_subject'),
    path('edit/<int:pk>/', views.edit_subject, name='edit_subject'),
    path('delete/<int:pk>/', views.delete_subject, name='delete_subject'),
    path('detail/<int:pk>/', views.detail_subject, name='detail_subject'),
    path('subject/teachers/', views.list_subject_teacher,
         name='list_subject_teacher'),

    path('teacher_subject/delete/<int:pk>/',
         views.delete_teacher_subject, name='delete_teacher_subject'),
]
