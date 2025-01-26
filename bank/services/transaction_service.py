from django.db import transaction
from django.utils.dateparse import parse_date
from bank.models import Wallet, Transaction
from decimal import Decimal
from datetime import datetime, time
# from django.utils import timezone
from django.utils.timezone import make_aware, is_naive


def transfer_funds(sender_user, receiver_username, amount):
    """Processa a transferência e evita duplicidade."""

    amount = Decimal(amount)
    if amount <= 0:
        raise ValueError("O valor da transferência deve ser maior que zero.")

    with transaction.atomic():
        sender_wallet = Wallet.objects.select_for_update().get(
            user=sender_user
        )
        receiver_wallet = Wallet.objects.select_for_update().get(
            user__username=receiver_username
        )

        if sender_wallet.balance < amount:
            raise ValueError("Saldo insuficiente para realizar "
                             "a transferência.")

        """"
        last_transaction = Transaction.objects.filter(
            sender=sender_wallet,
            receiver=receiver_wallet
        ).order_by().last()

        if last_transaction:
            now = timezone.now()

            if last_transaction.timestamp.tzinfo is None:
                last_transaction.timestamp = make_aware(
                    last_transaction.timestamp
                )

            time_difference = now - last_transaction.timestamp

            if (
                last_transaction.receiver == receiver_wallet and
                last_transaction.amount == amount and
                time_difference.total_seconds() < 60
            ):
                raise ValueError("Transação duplicada detectada. "
                                 "Aguarde antes de tentar novamente.")
        """

        sender_wallet.balance -= amount
        receiver_wallet.balance += amount
        sender_wallet.save()
        receiver_wallet.save()

        transaction_res = Transaction.objects.create(
            sender=sender_wallet,
            receiver=receiver_wallet,
            amount=amount
        )

    return transaction_res


def get_balance(user):
    """Retorna o saldo da carteira do usuário autenticado."""
    wallet = Wallet.objects.get(user=user)
    return wallet.balance


def add_funds(user, amount):
    """Adiciona fundos à carteira do usuário autenticado."""
    amount = Decimal(amount)
    if amount <= 0:
        raise ValueError("O valor deve ser maior que zero.")

    with transaction.atomic():
        user.wallet.balance += amount
        user.wallet.save()

    new_balance = get_balance(user)

    return {
        "new_balance": new_balance,
        "message": "Fundos adicionados com sucesso!"
    }


def get_user_transactions(user, start_date, end_date):
    """Retorna as transações de um usuário dentro de um intervalo de datas."""
    transactions = (
        Transaction.objects.filter(sender__user=user) |
        Transaction.objects.filter(receiver__user=user)
    )

    if start_date:
        start_date = parse_date(start_date)
        start_date = datetime.combine(start_date, time.min)
        if is_naive(start_date):
            start_date = make_aware(start_date)
        transactions = transactions.filter(timestamp__gte=start_date)

    if end_date:
        end_date = parse_date(end_date)
        end_date = datetime.combine(end_date, time.max)
        if is_naive(end_date):
            end_date = make_aware(end_date)
        transactions = transactions.filter(timestamp__lte=end_date)

    return [
        {
            "id": t.id,
            "sender": t.sender.user.username,
            "receiver": t.receiver.user.username,
            "amount": t.amount,
            "date": t.timestamp.strftime("%Y-%m-%d"),
        }
        for t in transactions
    ]
