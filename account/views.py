from django.shortcuts import render, redirect
# from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED

from account.serializer import AccountSerializer
from account.models import Account
import json


class AccountViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Account.objects.all().order_by('-date_joined')
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

@api_view(['GET'])
def me_view(request, format=None):
    user = request.user
    if user.is_authenticated:
        serializer = AccountSerializer(instance=user)
        return Response(serializer.data)
    content = {
        'User': 'Unauthorized'
    }
    return Response(content, status=HTTP_401_UNAUTHORIZED)
        
