from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_section, name='list_section'),
    path('detail/<int:pk>/', views.detail_section, name='detail_section'),
    path('create/', views.create_section, name='create_section'),
    path('edit/<int:pk>/', views.edit_section, name='edit_section'),
    path('delete/<int:pk>/', views.delete_section, name='delete_section'),
]
