from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework import status
from rulet.settings import MAIN_HOST

from account.serializer import AccountSerializer
from account.models import Account
from multiprocessing import Process

from django.http import HttpResponse
from django.shortcuts import render, redirect 
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages 
from django.contrib.auth import authenticate, login 
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.forms import AuthenticationForm 
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template 
from django.template import Context 
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View

from account.tokens import account_activation_token

from api.models import Category, MenuItem, Chef, Waiter

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

def send_confirmation(user):
    domain = MAIN_HOST + ':8000'
    htmly = get_template('account/Email.html') 
    d = { 
        'username': user.username,
        'domain': domain,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':account_activation_token.make_token(user),
    } 
    subject, from_email, to = 'Rulet email confirmation', 'isp2019test@gmail.com', user.email
    html_content = htmly.render(d) 
    msg = EmailMultiAlternatives(subject, html_content, from_email, [to]) 
    msg.attach_alternative(html_content, "text/html") 
    p = Process(target=msg.send)
    p.start()
    p.join()

def activate(request, uidb64, token):
    try:
        uid = int(urlsafe_base64_decode(uidb64))
        user = Account.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')