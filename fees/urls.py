from django.urls import path
from . import views

urlpatterns = [
    path('fee-types/', views.list_fee_types, name='list_fee_types'),
    path('fee-types/add/', views.create_fee_type, name='create_fee_type'),
    path('fee-types/edit/<int:pk>/', views.edit_fee_type, name='edit_fee_type'),
    path('fee-types/delete/<int:pk>/',
         views.delete_fee_type, name='delete_fee_type'),

    path('fee-payments/', views.list_fee_payments, name='list_fee_payments'),
    path('fee-payments/add/', views.create_fee_payment, name='create_fee_payment'),
    path('fee-payments/edit/<int:pk>/',
         views.edit_fee_payment, name='edit_fee_payment'),
    path('fee-payments/delete/<int:pk>/',
         views.delete_fee_payment, name='delete_fee_payment'),

    path('fee-payments/invoice/<int:pk>/', views.generate_invoice_pdf,
         name='generate_invoice_pdf'),  # New URL for PDF download
]
