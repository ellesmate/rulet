from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework import status
from rulet.settings import MAIN_HOST

from account.serializer import AccountSerializer
from account.models import Account
from multiprocessing import Process
import json


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
import random

from .tokens import account_activation_token
from .forms import UserRegisterForm, MenuItemDetailForm, MenuItemForm, CategoryForm, EmployeeForm

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
        

#################### index####################################### 
def index(request): 
    if (request.user.is_authenticated):
        colors = ['y', 'g', 'o', 's', 'r']
        employee = request.user.employee
        entity = employee.entity

        categories = list(Category.objects.filter(entity=entity))
        
        c = random.choices(colors, k=len(categories))

        ziped = tuple(zip(categories, c))
        print(ziped)

        return render(request, 'account/index.html', {'title':'index', 'ziped': ziped}) 

    return redirect('login')


class CategoryView(View):
    def dispatch(self, *args, **kwargs):
        method = self.request.POST.get('_method', '').lower()
        if method == 'put':
            return self.put(*args, **kwargs)
        if method == 'delete':
            return self.delete(*args, **kwargs)
        return super(CategoryView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):

        if (request.user.is_authenticated):

            employee = request.user.employee
            entity = employee.entity

            categories = Category.objects.filter(entity=entity)

            return render(request, 'account/category.html', {'title':'index', 'categories': categories}) 

        return redirect('index')
    
    def post(self, request, *args, **kwargs):

        data = request.POST.dict()
        data['entity'] = request.user.employee.entity
        form = CategoryForm(data, request.FILES)
        if form.is_valid():
            form.save()
        
        return redirect('index')


class CategoryDetailView(View):
    def dispatch(self, *args, **kwargs):
        method = self.request.POST.get('_method', '').lower()
        if method == 'put':
            return self.put(*args, **kwargs)
        if method == 'delete':
            return self.delete(*args, **kwargs)
        return super(CategoryDetailView, self).dispatch(*args, **kwargs)

    def get(self, request, pk, *args, **kwargs):
        if request.user.is_authenticated:
            employee = request.user.employee
            entity = employee.entity

            category = Category.objects.get(pk=pk)

            return render(request, 'account/category_edit.html', {'title':category.name, 'category': category}) 

        return redirect('index')


    def post(self, request, pk, *args, **kwargs):
        
        category = Category.objects.get(pk=pk)
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return redirect('index')

        content = {
            'error': form.errors
        }
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        Category.objects.get(pk=pk).delete()

        return redirect('index')


class MenuItemView(View):
    http_method_names = ['get', 'post', 'put', 'delete']

    def dispatch(self, *args, **kwargs):
        method = self.request.POST.get('_method', '').lower()
        if method == 'put':
            return self.put(*args, **kwargs)
        if method == 'delete':
            return self.delete(*args, **kwargs)
        return super(MenuItemView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        if (request.user.is_authenticated):

            category_id = request.GET.get('category')
            employee = request.user.employee
            entity = employee.entity
            title = 'Menu'

            menu_items = MenuItem.objects.filter(entity=entity)
            categories = Category.objects.filter(entity=entity)

            if category_id is not None:
                menu_items = menu_items.filter(category__id=category_id)
                title = Category.objects.get(pk=category_id).name

            return render(request, 'account/menu.html', {'title':title, 'menu_items': menu_items, 'categories': categories}) 

        return redirect('index')
    
    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        data['entity'] = request.user.employee.entity
        form = MenuItemForm(data, request.FILES)
        if form.is_valid():
            form.save()
        
        return redirect('index')
    

class MenuItemDetailView(View):

    def dispatch(self, *args, **kwargs):
        method = self.request.POST.get('_method', '').lower()
        if method == 'put':
            return self.put(*args, **kwargs)
        if method == 'delete':
            return self.delete(*args, **kwargs)
        return super(MenuItemDetailView, self).dispatch(*args, **kwargs)

    def get(self, request, pk, *args, **kwargs):
        if request.user.is_authenticated:
            employee = request.user.employee
            entity = employee.entity

            menuitem = MenuItem.objects.get(pk=pk)
            categories = Category.objects.filter(entity=entity)

            return render(request, 'account/menu_edit.html', {'title':menuitem.item_type, 'menuitem': menuitem, 'categories': categories}) 

        return redirect('index')

    def post(self, request, pk, *args, **kwargs):
        
        menuitem = MenuItem.objects.get(pk=pk)
        form = MenuItemDetailForm(request.POST, request.FILES, instance=menuitem)
        if form.is_valid():
            form.save()
            return redirect('index')

        content = {
            'error': form.errors
        }
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):

        MenuItem.objects.get(pk=pk).delete()

        return redirect('index')

class EmployeeView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            entity = request.user.employee.entity
            waiters = Waiter.objects.filter(employee__entity=entity)
            cooks = Chef.objects.filter(employee__entity=entity)

            return render(request, 'account/employee.html', {'title':'index', 'waiters': waiters, 'cooks': cooks}) 

        return redirect('index')

    def post(self, request, *args, **kwargs):

        data = request.POST.dict()
        position = data.get('position')

        if position not in ('waiter', 'cook'):
            return Response({'error': 'position is required field.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            account = Account.objects.get(email=data['email'])
        except Exception as err:
            return Response({'error': err}, status=status.HTTP_400_BAD_REQUEST)

        data['entity'] = request.user.employee.entity
        data['account'] = account
        
        form = EmployeeForm(data)
        if form.is_valid():
            employee = form.save()
            if position == 'waiter':
                Waiter.objects.create(employee=employee)
            elif position == 'cook':
                Cook.objects.create(employee=employee)
            
            return redirect('employee')

        content = {
            'error': form.errors
        }
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

class EmployeeDetailView(View):

    def dispatch(self, *args, **kwargs):
        method = self.request.POST.get('_method', '').lower()
        if method == 'put':
            return self.put(*args, **kwargs)
        if method == 'delete':
            return self.delete(*args, **kwargs)
        return super(EmployeeDetailView, self).dispatch(*args, **kwargs)

    def delete(self, request, pk, *args, **kwargs):

        Employee.objects.get(pk=pk).delete()

        return redirect('employee')

########### register here ##################################### 
def register(request): 
    if request.method == 'POST': 
        form = UserRegisterForm(request.POST) 
        if form.is_valid(): 
            user = form.save() 
            send_confirmation(user)

            messages.success(request, f'Your account has been created ! You are now able to log in') 
            return redirect('login') 
    else: 
        form = UserRegisterForm() 
    return render(request, 'account/register.html', {'form': form, 'title':'reqister here'}) 

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


################ login forms################################################### 
def Login(request): 
    if request.method == 'POST': 

        username = request.POST['username'] 
        password = request.POST['password'] 
        user = authenticate(request, username = username, password = password) 
        if user is not None: 
            form = login(request, user) 
            messages.success(request, f' wecome {username} !!') 
            return redirect('index') 
        else: 
            messages.info(request, f'account done not exit plz sign in') 
            return HttpResponse('Unauthorized', status=401)
    # form = AuthenticationForm() 
    # return render(request, 'account/login.html', {'form':form, 'title':'log in'}) 
    return render(request, 'account/login.html', {'title':'log in'}) 

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
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')