# from django.contrib.auth.models import User, Group
from account.models import Account
from rest_framework import serializers


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'password', 'email', 'username']
