from decimal import Decimal
from django import forms
from .models import Account


class TransactionForm(forms.Form):
    """Форма для ввода данных новой транзакции."""

    debit_account = forms.ModelChoiceField(
        queryset=Account.objects.all(), label="Дебет"
    )
    credit_account = forms.ModelChoiceField(
        queryset=Account.objects.all(), label="Кредит"
    )
    amount = forms.DecimalField(
        min_value=Decimal("0.01"), decimal_places=2, max_digits=18, label="Сумма"
    )
    description = forms.CharField(
        label="Описание", required=False, widget=forms.Textarea(attrs={"rows": 2})
    )

    def clean(self):
        data = super().clean()
        d = data.get("debit_account")
        c = data.get("credit_account")
        if d and c and d.pk == c.pk:
            raise forms.ValidationError("Дебет и кредит должны быть разными счетами.")
        return data
