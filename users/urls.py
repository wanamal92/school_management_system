from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # Admin-only user management views
    path('users/', views.user_list, name='user_list'),
    path('users/add/', views.user_create, name='user_create'),
    path('users/edit/<int:user_id>/', views.user_edit, name='user_edit'),
    path('users/delete/<int:user_id>/', views.user_delete, name='user_delete'),
    path('users/view/<int:user_id>/', views.user_detail, name='user_detail'),
    path('users/toggle-status/<int:user_id>/', views.toggle_user_status, name='toggle_user_status'),

    
    path('users/account/', views.profile_view, name='profile_view'),
    path('users/account/edit/', views.profile_edit, name='profile_edit'),
    path('force-password-change/', views.force_password_change, name='force_password_change'),

    path('users/audit-logs/', views.audit_log_list, name='audit_log_list'),

    path('users/unlock/<int:user_id>/', views.unlock_user, name='unlock_user'),


]
