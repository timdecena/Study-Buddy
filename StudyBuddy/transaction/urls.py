# transaction/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.transaction_management, name='transaction-management'),
    path('add/', views.add_transaction, name='add-transaction'),
    path('update/<int:transaction_id>/', views.update_transaction, name='update-transaction'),
    path('delete/<int:transaction_id>/', views.delete_transaction, name='delete-transaction'),
]
