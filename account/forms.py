# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from .models import Account
# # from django.contrib.auth.models import User

# class SignupForm(UserCreationForm):
#     email = forms.EmailField(max_length=200, help_text='Required')    
    
#     class Meta:
#         model = Account
#         fields = ('username', 'email', 'password1', 'password2')
from django import forms 
from django.contrib.auth.forms import UserCreationForm 
from .models import Account
from api.models import MenuItem, Category, Employee



class UserRegisterForm(UserCreationForm): 
    email = forms.EmailField() 
    # phone_no = forms.CharField(max_length = 20) 
    # first_name = forms.CharField(max_length = 20) 
    # last_name = forms.CharField(max_length = 20) 
    class Meta: 
        model = Account
        fields = ['username', 'email', 'password1', 'password2'] 


# class MenuItemDetailForm(forms.Form):
#     item_type = forms.CharField(label='item_type', max_length=30)
#     price = forms.IntegerField(label='price')
#     available = forms.BooleanField(label='available')
#     item_description = forms.TextField(label='item_description')
#     image = forms.ImageField(label='image')
#     size = forms.IntegerField(label='size')
#     category = froms.CharField(label='category', max_length=30)

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
