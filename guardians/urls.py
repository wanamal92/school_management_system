# guardians/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_guardian, name='list_guardian'),
    path('add/', views.add_guardian, name='add_guardian'),
    path('edit/<int:pk>/', views.edit_guardian, name='edit_guardian'),
    path('delete/<int:pk>/', views.delete_guardian, name='delete_guardian'),
    path('detail/<int:pk>/', views.detail_guardian, name='detail_guardian'),
    path('profile/', views.profile_guardian, name='profile_guardian'),
]
