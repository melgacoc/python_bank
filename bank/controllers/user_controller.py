from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.core.exceptions import ValidationError
from bank.services.user_service import (
    create_user,
    get_users,
    authenticate_user
)
from bank.serializers import UserSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        try:
            user, tokens = create_user(
                serializer.validated_data['username'],
                serializer.validated_data['password'],
                serializer.validated_data['email'],
                serializer.validated_data['cpf']
            )

            return Response({
                "message": "Usuário criado com sucesso!",
                "id": user.id,
                "token": tokens
            })
        except ValidationError as e:
            return Response({"error": str(e)}, status=400)
    return Response(serializer.errors, status=400)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    try:
        user, tokens = authenticate_user(username, password)
        return Response({
            "message": "Login realizado com sucesso!",
            "id": user.id,
            "token": tokens
        })
    except ValidationError as e:
        return Response({"error": str(e)}, status=401)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_users(request):
    users = get_users()
    return Response({"users": users})
