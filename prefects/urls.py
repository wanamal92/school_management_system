from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_prefects, name='list_prefects'),
    path('add/', views.create_prefect, name='create_prefect'),
    path('edit/<int:pk>/', views.edit_prefect, name='edit_prefect'),
    path('delete/<int:pk>/', views.delete_prefect, name='delete_prefect'),
]
