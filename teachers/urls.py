# teachers/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_teachers, name='list_teachers'),
    path('add/', views.add_teacher, name='add_teacher'),
    path('edit/<int:pk>/', views.edit_teacher, name='edit_teacher'),
    path('delete/<int:pk>/', views.delete_teacher, name='delete_teacher'),
    path('detail/<int:pk>/', views.detail_teacher, name='detail_teacher'),
    path('profile/', views.profile_teacher, name='profile_teacher'),
    path('export/leave-records/', views.export_teacher_leave_excel,
         name='export_leave_excel'),
    path('export/leave-report-pdf/', views.export_teacher_leave_pdf,
         name='export_teacher_leave_pdf'),

]
