import pytest
from django.urls import reverse
from account.models import Account
from account.forms import UserRegisterForm
from django.test import Client


@pytest.fixture
def user(db) -> Account:
    return Account.objects.create_user('email@gmail.com', 'username', 'aklflakjsdlf')

@pytest.fixture
def super_user(db) -> Account:
    return Account.objects.create_superuser('email@gmail.com', 'username', 'secret_password')

def test_check_password(db, user: Account) -> None:
    user.set_password('tApo4eck')
    assert user.check_password('tApo4eck') is True

def test_should_not_check_unusable_password(db, user: Account):
    user.set_password("secret")
    user.set_unusable_password()
    assert user.check_password("secret") is False

def test_redirect(client):
    url = reverse('index')
    response = client.get(url)
    assert response.status_code == 302

@pytest.mark.parametrize("email,username,password,password2,error_field",
                          [('Nonedefault', 'test', 'test', 'test', "email"),
                          ('Nonedefault@gmail.com', 'Nonedefault', 'Nonedefault', 'test', "password2"), ])
def test_registration_form(db, email, username, password, password2, error_field):
    form_data = {'username': username, 'password': password,
                                     'password2': password2, 'email': email}
    form = UserRegisterForm(data=form_data)
    assert form.has_error(error_field)

def test_login_form(db, super_user):
    c = Client()
    response = c.get('/login/')
    assert response.status_code == 200 
    response = c.post('/login/', {'username': 'default0', 'password': 'default'})
    assert response.status_code == 401
    response = c.post('/login/', {'username': 'test', 'password': 'test'})
    assert response.status_code == 401
    response = c.post('/login/', {'username': super_user.email, 'password': 'secret_password'})
    assert response.status_code == 302