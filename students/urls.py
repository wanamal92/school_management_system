from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_students, name='list_students'),
    path('add/', views.create_student, name='create_student'),
    path('edit/<int:student_id>/', views.edit_student, name='edit_student'),
    path('delete/<int:student_id>/', views.delete_student, name='delete_student'),
    path('view/<int:student_id>/', views.detail_student, name='detail_student'),
    path('profile/', views.profile_student, name='profile_student'),

]
