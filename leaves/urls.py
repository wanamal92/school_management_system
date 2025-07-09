from django.urls import path
from . import views

urlpatterns = [
    path('teacher/leave-requests/', views.teacher_leave_requests,
         name='teacher_leave_requests'),
    path('teacher/leave-requests/create/',
         views.create_leave_request, name='create_leave_request'),
    path('teacher/leave-requests/<int:pk>/update/',
         views.edit_leave_request, name='edit_leave_request'),
    path('teacher/leave-requests/<int:pk>/delete/',
         views.delete_leave_request, name='delete_leave_request'),

    path('admin/leave-requests/', views.admin_leave_requests,
         name='admin_leave_requests'),
    path('admin/leave-requests/<int:pk>/approve-reject/',
         views.approve_reject_leave, name='approve_reject_leave'),

    path('admin/leave-allocation/', views.list_leave_allocations,
         name='list_leave_allocations'),
    path('admin/leave-allocation/create/',
         views.create_leave_allocation, name='create_leave_allocation'),
    path('admin/leave-allocation/<int:pk>/update/',
         views.edit_leave_allocation, name='edit_leave_allocation'),
    path('admin/leave-allocation/<int:pk>/delete/',
         views.delete_leave_allocation, name='delete_leave_allocation'),

    path('admin/leave-types/', views.list_leave_types, name='list_leave_types'),
    path('admin/leave-types/create/',
         views.create_leave_type, name='create_leave_type'),
    path('admin/leave-types/<int:pk>/update/',
         views.edit_leave_type, name='edit_leave_type'),
    path('admin/leave-types/<int:pk>/delete/',
         views.delete_leave_type, name='delete_leave_type'),
]
