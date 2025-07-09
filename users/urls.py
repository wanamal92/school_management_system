from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # Admin-only user management views
    path('users/', views.list_users, name='list_users'),
    path('users/add/', views.create_user, name='create_user'),
    path('users/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('users/view/<int:user_id>/', views.detail_user, name='detail_user'),
    path('users/toggle-status/<int:user_id>/',
         views.toggle_user_status, name='toggle_user_status'),


    path('users/account/', views.view_profile, name='view_profile'),
    path('users/account/edit/', views.edit_profile, name='edit_profile'),
    path('force-password-change/', views.force_password_change,
         name='force_password_change'),

    path('users/audit-logs/', views.audit_log_list, name='audit_log_list'),

    path('users/unlock/<int:user_id>/', views.unlock_user, name='unlock_user'),


]
