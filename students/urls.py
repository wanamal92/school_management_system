from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_list, name='student_list'),
    path('add/', views.student_create, name='student_create'),
    path('edit/<int:student_id>/', views.student_edit, name='student_edit'),
    path('delete/<int:student_id>/', views.student_delete, name='student_delete'),
    path('view/<int:student_id>/', views.student_detail, name='student_detail'),
    path('profile/', views.student_profile, name='student_profile'),

]
