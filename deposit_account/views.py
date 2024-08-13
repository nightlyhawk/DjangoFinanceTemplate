from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.views import APIView
from .models import Account, Transfer
from .serializers import AccountSerializer, TransferSerializer
from .decorators import error_catch
from django.db.models import Q
# Create your views here.

class AccountDetails(APIView):
    parser_classes = [JSONParser]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        user = request.user
        account = Account.objects.get(user=user)
        serializer = AccountSerializer(account)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@error_catch
def TransferFunds(request, pk):
    user = request.user
    account = Account.objects.get(user=user)
    receiver=Account.objects.get(id=pk)
    amount = request.data['amount']
    transfer = Transfer.objects.create(sender=account, receiver=receiver, amount=amount)
    account.balance -= amount
    account.save()
    receiver.balance += amount
    receiver.save()
    return Response({"message":"success"}, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])    
@error_catch
def TransferHistory(request):
    user=request.user
    account = Account.objects.get(user=user)
    transfers = Transfer.objects.filter((Q (sender=account) | Q (receiver=account))).all()
    serializer = TransferSerializer(transfers, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)