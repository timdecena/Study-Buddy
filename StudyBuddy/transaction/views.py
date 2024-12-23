from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Transaction
from .forms import TransactionForm
from tutors.models import Tutor
from students.models import Student

def transaction_management(request):
    form = TransactionForm()
    transactions = Transaction.objects.select_related('tutor', 'student').all()  # Fetch related tutor and student
    tutors = Tutor.objects.all()  # Fetch all tutors for the dropdown
    students = Student.objects.all()  # Fetch all students for the dropdown
    return render(request, 'transaction_management.html', {
        'form': form,
        'transactions': transactions,
        'tutors': tutors,
        'students': students  # Add students to the context
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
                'tutor_id': transaction.tutor.id,
                'student_name': transaction.student.fullname,
                'student_id': transaction.student.student_id
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
                'tutor_id': transaction.tutor.id,
                'student_name': transaction.student.fullname,
                'student_id': transaction.student.student_id
            })
    return JsonResponse({'error': 'Invalid data'}, status=400)

def delete_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, pk=transaction_id)
    transaction.delete()
    return JsonResponse({'id': transaction_id})
