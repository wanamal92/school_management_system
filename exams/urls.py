# exams/urls.py
from django.urls import path
from . import views

urlpatterns = [
     path('list_exam_session/', views.list_exam_session, name='list_exam_session'),
    path('create_exam_session/', views.create_exam_session, name='create_exam_session'),
    path('edit_exam_session/<int:pk>/', views.edit_exam_session, name='edit_exam_session'),
    path('delete_exam_session/<int:pk>/', views.delete_exam_session, name='delete_exam_session'),
    path('detail_exam_session/<int:pk>/', views.detail_exam_session, name='detail_exam_session'),

    path('list_exam/', views.list_exam, name='list_exam'),
    path('create_exam/', views.create_exam, name='create_exam'),    
    path('edit_exam/<int:pk>/', views.edit_exam, name='edit_exam'),  
    path('delete_exam/<int:pk>/', views.delete_exam, name='delete_exam'),  
    path('detail_exam/<int:pk>/', views.detail_exam, name='detail_exam'),  

    path('list_exam_attendee/', views.list_exam_attendee, name='list_exam_attendee'),
    path('create_exam_attendee/', views.create_exam_attendee, name='create_exam_attendee'),
    path('edit_exam_attendee/<int:pk>/', views.edit_exam_attendee, name='edit_exam_attendee'),
    path('delete_exam_attendee/<int:pk>/', views.delete_exam_attendee, name='delete_exam_attendee'),
    path('detail_exam_attendee/<int:pk>/', views.detail_exam_attendee, name='detail_exam_attendee'),
    
]
