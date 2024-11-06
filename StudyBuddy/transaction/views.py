from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Transaction
from .forms import TransactionForm
from tutors.models import Tutor

def transaction_management(request):
    form = TransactionForm()
    transactions = Transaction.objects.select_related('tutor').all()  # Fetch related tutor
    tutors = Tutor.objects.all()  # Fetch all tutors for the dropdown
    return render(request, 'transaction_management.html', {
        'form': form,
        'transactions': transactions,
        'tutors': tutors
    })

def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save()
            return JsonResponse({
                'id': transaction.transaction_id,
                'method': transaction.payment_method,
                'amount': transaction.payment_amount,
                'tutor_last_name': transaction.tutor.last_name,
                'tutor_id': transaction.tutor.id
            })
    return JsonResponse({'error': 'Invalid data'}, status=400)

def update_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, pk=transaction_id)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            transaction = form.save()
            return JsonResponse({
                'id': transaction.transaction_id,
                'method': transaction.payment_method,
                'amount': transaction.payment_amount,
                'tutor_last_name': transaction.tutor.last_name,
                'tutor_id': transaction.tutor.id
            })
    return JsonResponse({'error': 'Invalid data'}, status=400)

def delete_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, pk=transaction_id)
    transaction.delete()
    return JsonResponse({'id': transaction_id})
