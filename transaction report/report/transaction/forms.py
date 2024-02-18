from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['transaction_type', 'mode_of_payment', 'amount', 'category', 'status']
