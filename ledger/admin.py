from django.contrib import admin
from .models import BalanceArticle, BalanceGroup, Account, Transaction


@admin.register(BalanceArticle)
class BalanceArticleAdmin(admin.ModelAdmin):
    """Настройки админки для модели BalanceArticle."""

    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(BalanceGroup)
class BalanceGroupAdmin(admin.ModelAdmin):
    """Настройки админки для модели BalanceGroup."""

    list_display = ("id", "article", "name")
    list_filter = ("article",)
    search_fields = ("name",)


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    """Настройки админки для модели Account."""

    list_display = ("id", "number", "name", "type", "group", "balance")
    list_filter = ("type", "group__article", "group")
    search_fields = ("number", "name")


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """Настройки админки для модели Transaction."""

    list_display = (
        "id",
        "created_at",
        "amount",
        "debit_account",
        "credit_account",
        "posted",
        "description",
    )
    list_filter = (
        "posted",
        "debit_account__group__article",
        "credit_account__group__article",
    )
    search_fields = ("description",)
    readonly_fields = ("posted",)
