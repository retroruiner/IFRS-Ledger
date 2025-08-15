from decimal import Decimal
import random
from django.db import models


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
