# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_documents, name='list_documents'),
    path('add/', views.create_document, name='create_document'),
    path('edit/<int:pk>/', views.edit_document, name='edit_document'),
    path('delete/<int:pk>/', views.delete_document, name='delete_document'),
    path('download/<int:pk>/', views.download_document, name='download_document'),  
]
