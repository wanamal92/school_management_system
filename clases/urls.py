from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_class, name='list_class'),
    path('detail/<int:pk>/', views.detail_class, name='detail_class'),
    path('create/', views.create_class, name='create_class'),
    path('edit/<int:pk>/', views.edit_class, name='edit_class'),
    path('delete/<int:pk>/', views.delete_class, name='delete_class'),
]
