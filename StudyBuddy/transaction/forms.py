from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['payment_method', 'payment_amount', 'tutor']  # Include tutor here
