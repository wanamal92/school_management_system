from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_health_records, name='list_health_records'),
    path('health-records/create/', views.create_health_record, name='create_health_record'),
    path('health-records/update/<int:pk>/', views.update_health_record, name='update_health_record'),
    path('health-records/delete/<int:pk>/', views.delete_health_record, name='delete_health_record'),
]
