from django.urls import path
from .views import transaction_report, transaction_edit, transaction_delete

urlpatterns = [
    path('transaction-report/', transaction_report, name='transaction_report'),
    path('transaction/<int:pk>/edit/', transaction_edit, name='transaction_edit'),
    path('transaction/<int:pk>/delete/', transaction_delete, name='transaction_delete'),
]