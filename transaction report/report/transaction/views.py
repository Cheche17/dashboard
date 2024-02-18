from django.shortcuts import render, redirect, get_object_or_404
from .models import Transaction
from .forms import TransactionForm

def transaction_report(request):
    transactions = Transaction.objects.all()
    weekly_totals = Trnasaction.objects.values('date__week').annotate(total=sum('amount'))
    return render(request, 'transaction_report.html', {'transactions': transactions, 'weekly_totals': weekly_totals})

def transaction_edit(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('transaction_report')
    else:
        form = TransactionForm(instance=transaction)
    return render(request, 'transaction_edit.html', {'form': form})

def transaction_delete(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        transaction.delete()
        return redirect('transaction_report')
    return render(request, 'transaction_delete.html', {'transaction': transaction})