from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from bank.models import User


class UserViewTests(TestCase):
    def tearDown(self):
        """Limpa o ambiente após cada teste."""
        User.objects.filter(email=self.user_data['email']).delete()

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

    def test_register_user(self):
        """Testa o endpoint de registro de usuário."""
        url = '/api/register/'
        data = {
            "username": "novo_usuario",
            "password": "novasenha123",
            "email": "novo@email.com",
            "cpf": "42824013036"
        }
        response = self.client.post(url, data, format='json')

        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_user(self):
        """Testa o endpoint de login de usuário."""
        url = '/api/login/'
        data = {
            "username": self.user_data['username'],
            "password": self.user_data['password']
        }
        response = self.client.post(url, data, format='json')

        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_users_view(self):
        """Testa o endpoint para listar usuários com autenticação."""
        self.client.force_authenticate(user=self.user)
        url = '/api/users/'
        response = self.client.get(url, format='json')

        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)