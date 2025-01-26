from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from bank.services.transaction_service import (
    transfer_funds,
    get_balance,
    get_user_transactions,
    add_funds
)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def transfer(request):
    sender_user = request.user
    receiver_username = request.data.get("receiver")
    amount = request.data.get("amount")

    try:
        transaction = transfer_funds(sender_user, receiver_username, amount)
        response_data = {
            "message": "Transferência realizada com sucesso!",
            "transaction_id": transaction.id,
            "new_balance": get_balance(sender_user)
        }
        return Response(response_data)
    except ValueError as e:
        return Response({"error": str(e)}, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_funds_to_wallet(request):
    """Controller para adicionar fundos à carteira."""
    amount = request.data.get("amount")
    user = request.user

    try:
        response_data = add_funds(user, amount)
        return Response(response_data)
    except ValueError as e:
        return Response({"error": str(e)}, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_balance(request):
    """Consulta o saldo da carteira do usuário autenticado."""
    balance = get_balance(request.user)
    return Response({"balance": balance})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_transactions(request):
    """Lists user transactions with optional date filter."""
    start_date = request.data.get("start_date")
    end_date = request.data.get("end_date")

    transactions = get_user_transactions(request.user, start_date, end_date)

    return Response(transactions)
