from django.shortcuts import render, redirect
# from django.contrib.auth.models import User, Group
from account.models import Account
from rest_framework import viewsets
from rest_framework import permissions
from account.serializer import AccountSerializer


class AccountViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Account.objects.all().order_by('-date_joined')
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]
