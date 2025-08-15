from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from .models import BalanceArticle, BalanceGroup, Account, Transaction


class LedgerTests(TestCase):
    def setUp(self):
        a = BalanceArticle.objects.create(name="Активы")
        p = BalanceArticle.objects.create(name="Пассивы")
        g_cash = BalanceGroup.objects.create(article=a, name="Денежные средства")
        g_clients = BalanceGroup.objects.create(article=a, name="Счета клиентов")
        g_capital = BalanceGroup.objects.create(article=p, name="Капитал")

        self.cash = Account.objects.create(
            group=g_cash, number="1000000001", name="Касса", type=Account.Type.ASSET
        )
        self.clients = Account.objects.create(
            group=g_clients,
            number="1000000002",
            name="Счета клиентов",
            type=Account.Type.ASSET,
        )
        self.capital = Account.objects.create(
            group=g_capital,
            number="3000000001",
            name="Уставной капитал",
            type=Account.Type.LIABILITY,
        )

    def test_asset_to_asset(self):
        Transaction.post_transaction(
            debit=self.cash,
            credit=self.clients,
            amount=Decimal("100.00"),
            description="Перекладка",
        )
        self.cash.refresh_from_db()
        self.clients.refresh_from_db()
        self.assertEqual(self.cash.balance, Decimal("100.00"))  # актив по дебету +
        self.assertEqual(self.clients.balance, Decimal("-100.00"))  # актив по кредиту -

    def test_asset_to_liability(self):
        Transaction.post_transaction(
            debit=self.cash, credit=self.capital, amount=Decimal("300.00")
        )
        self.cash.refresh_from_db()
        self.capital.refresh_from_db()
        self.assertEqual(self.cash.balance, Decimal("300.00"))  # актив по дебету +
        self.assertEqual(self.capital.balance, Decimal("300.00"))  # пассив по кредиту +

    def test_liability_to_asset(self):
        Transaction.post_transaction(
            debit=self.capital, credit=self.cash, amount=Decimal("50.00")
        )
        self.capital.refresh_from_db()
        self.cash.refresh_from_db()
        self.assertEqual(self.capital.balance, Decimal("-50.00"))  # пассив по дебету -
        self.assertEqual(self.cash.balance, Decimal("-50.00"))  # актив по кредиту -

    def test_form_view_creates_transaction(self):
        resp = self.client.get(reverse("transaction_create"))
        self.assertEqual(resp.status_code, 200)

        resp = self.client.post(
            reverse("transaction_create"),
            data={
                "debit_account": self.cash.id,
                "credit_account": self.clients.id,
                "amount": "123.45",
                "description": "Тест форма",
            },
        )
        self.assertEqual(resp.status_code, 302)

        self.cash.refresh_from_db()
        self.clients.refresh_from_db()
        self.assertEqual(self.cash.balance, Decimal("123.45"))
        self.assertEqual(self.clients.balance, Decimal("-123.45"))
