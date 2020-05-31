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



class UserRegisterForm(UserCreationForm): 
	email = forms.EmailField() 
	# phone_no = forms.CharField(max_length = 20) 
	# first_name = forms.CharField(max_length = 20) 
	# last_name = forms.CharField(max_length = 20) 
	class Meta: 
		model = Account
		fields = ['username', 'email', 'password1', 'password2'] 
