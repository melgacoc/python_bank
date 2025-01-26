from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from bank.models import Wallet


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        User = get_user_model()

        if not User.objects.filter(username="admin").exists():
            admin = User.objects.create_superuser(
                "admin",
                "admin@email.com",
                "admin",
                cpf="90887605001"
            )
            claudio = User.objects.create_user(
                "Claudio",
                "claudio@email.com",
                "1234",
                cpf="52662231033"
            )

            Wallet.objects.create(user=admin, balance=1000)
            Wallet.objects.create(user=claudio, balance=1000)

        self.stdout.write(
            self.style.SUCCESS("Banco de dados populado com sucesso!")
        )
