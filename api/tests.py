import pytest
from django.urls import reverse



def test_superuser_category_view(admin_client):
    url = reverse('category-list', args=[1])
    response = admin_client.get(url)
    assert response.status_code == 200

def test_unathorized_user_category_view(client):
    url = reverse('category-list', args=[1])
    response = client.get(url)
    assert response.status_code == 401
