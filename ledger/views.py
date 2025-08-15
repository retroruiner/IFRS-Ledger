from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from .models import Account, Transaction
from .forms import TransactionForm


def accounts_list(request):
    """Выводит список всех счетов с их группами и статьями баланса."""
    accounts = Account.objects.select_related("group", "group__article").all()
    return render(request, "ledger/accounts_list.html", {"accounts": accounts})


def transactions_list(request):
    """Выводит список всех транзакций с дебетовым и кредитовым счетом."""
    txs = Transaction.objects.select_related("debit_account", "credit_account").all()
    return render(request, "ledger/transactions_list.html", {"transactions": txs})


def transaction_create(request):
    """Создаёт новую транзакцию из формы, проводит её и сохраняет в базе."""
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            debit = form.cleaned_data["debit_account"]
            credit = form.cleaned_data["credit_account"]
            amount: Decimal = form.cleaned_data["amount"]
            description = form.cleaned_data["description"]
            try:
                Transaction.post_transaction(
                    debit=debit, credit=credit, amount=amount, description=description
                )
            except ValueError as e:
                form.add_error(None, str(e))
            else:
                messages.success(request, "Транзакция успешно проведена.")
                return redirect(reverse("transactions_list"))
    else:
        form = TransactionForm()
    return render(request, "ledger/transaction_form.html", {"form": form})
