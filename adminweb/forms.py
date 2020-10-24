from django import forms 
from django.contrib.auth.forms import UserCreationForm 
from account.models import Account
from api.models import MenuItem, Category, Employee


class UserRegisterForm(UserCreationForm): 
    email = forms.EmailField()
    class Meta: 
        model = Account
        fields = ['username', 'email', 'password1', 'password2'] 

class MenuItemDetailForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['item_type', 'price', 'available', 'item_description', 'image', 'size', 'category']

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['item_type', 'price', 'available', 'item_description', 'image', 'size', 'category', 'entity']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'image', 'entity']

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['first_name', 'middle_name', 'last_name',  'entity', 'account']
