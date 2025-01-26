from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def create_user(username, password, email, cpf):
    if User.objects.filter(email=email).exists():
        raise ValidationError("O email já está em uso.")
    if User.objects.filter(cpf=cpf).exists():
        raise ValidationError("O CPF já está cadastrado.")
    hash_password = make_password(password)
    user = User(
        username=username,
        email=email,
        cpf=cpf,
        password=hash_password
    )
    user.save()

    tokens = get_tokens_for_user(user)
    return user, tokens


def authenticate_user(username, password):
    try:
        user = get_user_model().objects.get(username=username)
        if not check_password(password, user.password):
            raise ValidationError("Usuário ou senha inválidos.")
    except get_user_model().DoesNotExist:
        raise ValidationError("Usuário ou senha inválidos.")

    tokens = get_tokens_for_user(user)
    return user, tokens


def get_users():
    return User.objects.values('id', 'username')
