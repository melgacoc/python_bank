from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from bank.models.user import User
from validate_docbr import CPF


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'cpf', 'password']

    def validate_username(self, value):
        if len(value) < 4:
            raise serializers.ValidationError(
                "O nome de usuário precisa ter no mínimo 4 caracteres."
            )
        if len(value) > 150:
            raise serializers.ValidationError(
                "O nome de usuário não pode ter mais de 150 caracteres."
            )
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError(
                "A senha precisa ter no mínimo 8 caracteres."
            )
        return value

    def validate_email(self, value):
        try:
            EmailValidator()(value)
        except ValidationError:
            raise serializers.ValidationError("Email inválido.")

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este email já está em uso.")
        return value

    def validate_cpf(self, value):
        cpf = CPF()

        if not cpf.validate(value):
            raise serializers.ValidationError(
                "CPF inválido."
            )

        if not value.isdigit():
            raise serializers.ValidationError(
                "O CPF deve conter apenas números."
            )

        if User.objects.filter(cpf=value).exists():
            raise serializers.ValidationError(
                "Este CPF já está em uso."
            )

        return value
