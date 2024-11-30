from django import forms
from .models import Transaction

from students.models import Student  # Import the Student model

class TransactionForm(forms.ModelForm):
    student = forms.ModelChoiceField(queryset=Student.objects.all(), empty_label="Select Student")  # New Field

    class Meta:
        model = Transaction
        fields = ['payment_method', 'payment_amount', 'tutor', 'student']
