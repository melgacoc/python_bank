from django.db import models
from django.utils.timezone import now
from .user import User


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.user.username}'s Wallet"


class Transaction(models.Model):
    sender = models.ForeignKey(
        Wallet, related_name="sent_transactions", on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        Wallet, related_name="received_transactions", on_delete=models.CASCADE
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    transaction_date = models.DateField(default=now)

    def __str__(self):
        return (
            f"Transaction from {self.sender.user.username} to "
            f"{self.receiver.user.username} of amount {self.amount}"
        )
