from __future__ import annotations
import random
from decimal import Decimal
from django.db import models, transaction
from django.utils import timezone


class BalanceArticle(models.Model):
    """Статья баланса"""

    name = models.CharField(max_length=200, unique=True)

    class Meta:
        verbose_name = "Статья баланса"
        verbose_name_plural = "Статьи баланса"

    def __str__(self) -> str:
        return self.name


class BalanceGroup(models.Model):
    """Балансовая группа"""

    article = models.ForeignKey(
        BalanceArticle, on_delete=models.PROTECT, related_name="groups"
    )
    name = models.CharField(max_length=200)

    class Meta:
        unique_together = ("article", "name")
        verbose_name = "Балансовая группа"
        verbose_name_plural = "Балансовые группы"

    def __str__(self) -> str:
        return f"{self.article} / {self.name}"


def generate_account_number() -> str:
    """10 случайных цифр, уникальность гарантируется unique=True."""
    return "".join(random.choices("0123456789", k=10))


class Account(models.Model):
    class Type(models.TextChoices):
        ASSET = "ASSET", "Актив"
        LIABILITY = "LIABILITY", "Пассив"
        BOTH = "BOTH", "Активно-пассивный"

    group = models.ForeignKey(
        BalanceGroup, on_delete=models.PROTECT, related_name="accounts"
    )
    number = models.CharField(
        max_length=10, unique=True, default=generate_account_number
    )
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=10, choices=Type.choices)

    balance = models.DecimalField(
        max_digits=18, decimal_places=2, default=Decimal("0.00")
    )

    class Meta:
        ordering = ("number",)
        verbose_name = "Счёт"
        verbose_name_plural = "Счета"

    def __str__(self) -> str:
        return f"{self.number} {self.name} ({self.get_type_display()})"


class Transaction(models.Model):
    """Транзакция между двумя счетами."""

    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    description = models.CharField(max_length=500, blank=True)

    debit_account = models.ForeignKey(
        Account, on_delete=models.PROTECT, related_name="debit_transactions"
    )
    credit_account = models.ForeignKey(
        Account, on_delete=models.PROTECT, related_name="credit_transactions"
    )

    amount = models.DecimalField(max_digits=18, decimal_places=2)
    posted = models.BooleanField(default=False)

    class Meta:
        ordering = ("-created_at", "id")
        verbose_name = "Транзакция"
        verbose_name_plural = "Транзакции"

    def __str__(self) -> str:
        return f"{self.created_at:%d-%m-%Y %H:%M} {self.amount} {self.debit_account} <- {self.credit_account}"

    @staticmethod
    def _apply_side_effect(acc: Account, side: str, amount: Decimal) -> None:
        """Изменяет баланс счета в зависимости от стороны проводки."""

        if acc.type == Account.Type.ASSET:
            delta = amount if side == "DEBIT" else -amount
        elif acc.type == Account.Type.LIABILITY:
            delta = -amount if side == "DEBIT" else amount
        else:  # BOTH
            delta = amount if side == "DEBIT" else -amount

        acc.balance = (acc.balance or Decimal("0")) + delta
        acc.save(update_fields=["balance"])

    @classmethod
    def post_transaction(
        cls, *, debit: Account, credit: Account, amount: Decimal, description: str = ""
    ) -> "Transaction":
        """Создаёт новую транзакцию между двумя счетами и сразу изменяет их балансы."""
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной.")
        if debit.pk == credit.pk:
            raise ValueError("Дебет и кредит не могут совпадать.")

        with transaction.atomic():
            ids = sorted([debit.pk, credit.pk])
            locked = Account.objects.select_for_update().filter(pk__in=ids).in_bulk()
            debit_locked = locked[debit.pk]
            credit_locked = locked[credit.pk]

            tx = cls.objects.create(
                debit_account=debit_locked,
                credit_account=credit_locked,
                amount=amount,
                description=description,
                posted=False,
            )

            cls._apply_side_effect(debit_locked, "DEBIT", amount)
            cls._apply_side_effect(credit_locked, "CREDIT", amount)

            tx.posted = True
            tx.save(update_fields=["posted"])
            return tx
