from django.shortcuts import render

from .models import Account, Transaction


def accounts_list(request):
    accounts = Account.objects.select_related("group", "group__article").all()
    return render(request, "ledger/accounts_list.html", {"accounts": accounts})


def transactions_list(request):
    txs = Transaction.objects.select_related("debit_account", "credit_account").all()
    return render(request, "ledger/transactions_list.html", {"transactions": txs})
