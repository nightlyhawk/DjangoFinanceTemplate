from rest_framework import serializers
from .models import Account, Transfer
from user.models import NewUser
from user.serializers import NewUserSerializer

class AccountSerializer(serializers.ModelSerializer):
    user = NewUserSerializer(read_only=True)

    class Meta:
        model = Account
        fields = ('id', 'user', 'transfers', 'balance')

    
    def create(self, **validated_data):
        user = validated_data.pop('user')
        account = Account.objects.create(user=user, **validated_data)

        return account
    
class TransferSerializer(serializers.ModelSerializer):
    sender = AccountSerializer()
    receiver = AccountSerializer()

    class Meta:
        model = Transfer
        fields = ('id', 'sender', 'receiver', 'amount')