from django.urls import path
from . import views



urlpatterns = [
    path('', views.list_competitions, name='list_competitions'),
    path('create/', views.create_competition, name='create_competition'),
    path('edit/<int:pk>/', views.edit_competition, name='edit_competition'),
    path('delete/<int:pk>/', views.delete_competition, name='delete_competition'),
    
    path('results/', views.list_competition_results, name='list_competition_results'),
    path('results/create/', views.create_competition_result, name='create_competition_result'),
    path('results/edit/<int:pk>/', views.edit_competition_result, name='edit_competition_result'),
    path('results/delete/<int:pk>/', views.delete_competition_result, name='delete_competition_result'),
]
