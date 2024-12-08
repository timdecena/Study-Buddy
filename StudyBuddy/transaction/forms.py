from django import forms
from .models import Transaction
from students.models import Student  # Import the Student model
from tutors.models import Tutor
from friend_requests.models import FriendRequest

class TransactionForm(forms.ModelForm):
    PAYMENT_METHOD_CHOICES = [
        ('GCash', 'GCash'),
        ('PayMaya', 'PayMaya'),
        ('Credit Card', 'Credit Card'),
        ('Bank Transfer', 'Bank Transfer'),
        ('PayPal', 'PayPal'),
        ('Cash', 'Cash'),
    ]

    payment_method = forms.ChoiceField(
        choices=PAYMENT_METHOD_CHOICES, 
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Transaction
        fields = ['payment_method', 'payment_amount', 'tutor']
        widgets = {
            'payment_amount': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        student = kwargs.pop('student', None)
        super().__init__(*args, **kwargs)
        if student:
            self.fields['tutor'].queryset = Tutor.objects.filter(
                id__in=FriendRequest.objects.filter(
                    sender_student=student, status='accepted'
                ).values_list('receiver_tutor', flat=True)
            )
