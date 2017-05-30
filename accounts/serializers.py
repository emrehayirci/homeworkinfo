from rest_framework import serializers
from .models import Accounts


class AccountsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Accounts
        fields = ('iban', 'created_at', 'currency_type', 'user', 'amount')


# class APISerializer(serializers.Serializer):

