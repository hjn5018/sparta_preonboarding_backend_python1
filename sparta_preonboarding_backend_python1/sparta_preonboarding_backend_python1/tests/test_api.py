import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user():
    User = get_user_model()
    return User.objects.create_user(
        username='testuser',
        password='testpassword',
        nickname='testnickname',
    )

@pytest.mark.django_db
def test_signup(api_client):
    url = '/signup/'
    data = {
        'username': 'newuser',
        'password': 'newpassword',
        'nickname': 'newnickname',
    }

    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['username'] == data['username']
    assert response.data['nickname'] == data['nickname']
    assert 'roles' in response.data

@pytest.mark.django_db
def test_login(api_client, create_user):
    url = '/login/'
    data = {
        'username': 'testuser',
        'password': 'testpassword',
    }

    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert 'token' in response.data