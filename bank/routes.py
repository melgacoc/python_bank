from django.urls import path
from bank.controllers.user_controller import register, get_all_users, login
from bank.controllers.transaction_controller import (
    transfer,
    check_balance,
    list_transactions,
    add_funds_to_wallet
)

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('users/', get_all_users, name='get_users'),
    path('add-funds/', add_funds_to_wallet, name='add_funds'),
    path('transfer/', transfer, name='transfer'),
    path('balance/', check_balance, name='balance'),
    path('transactions/', list_transactions, name='transactions'),
]
