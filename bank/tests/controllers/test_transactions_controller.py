from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from bank.models import User, Wallet


class TransactionViewTests(TestCase):
    def setUp(self):
        """Configura o ambiente antes de cada teste."""
        self.client = APIClient()
        self.user_data = {
            "username": "fulano",
            "password": "testpassword123",
            "email": "fulano@email.com",
            "cpf": "26970980030"
        }
        self.user = User.objects.create_user(**self.user_data)
        self.client.force_authenticate(user=self.user)
        self.user_wallet = Wallet.objects.create(user=self.user, balance=0)

        self.receiver_data = {
            "username": "admin",
            "password": "adminpassword123",
            "email": "admin@email.com",
            "cpf": "42824013036"
        }
        self.receiver = User.objects.create_user(**self.receiver_data)
        self.receiver_wallet = Wallet.objects.create(
            user=self.receiver, balance=0
        )

    def test_transfer_funds(self):
        """Testa o endpoint de transferência de fundos."""
        url = '/api/add-funds/'
        data = {
            "amount": 1000
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = '/api/transfer/'
        data = {
            "receiver": self.receiver.username,
            "amount": 100
        }
        response = self.client.post(url, data, format='json')

        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_check_balance(self):
        """Testa o endpoint de consulta de saldo."""
        url = '/api/balance/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_transactions(self):
        """Testa o endpoint de listagem de transações."""
        url = '/api/transactions/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)