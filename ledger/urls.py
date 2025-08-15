from django.urls import path
from . import views

urlpatterns = [
    path("", views.accounts_list, name="accounts_list"),
    path("transactions/", views.transactions_list, name="transactions_list"),
    path("transactions/new/", views.transaction_create, name="transaction_create"),
]
