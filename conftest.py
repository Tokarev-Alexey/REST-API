import pytest
from users.models import ProfileUser
from rest_framework.test import APIClient


@pytest.fixture
def basic_user():
    """Фикстура создает одного пользователя с фиксированными данными"""
    return ProfileUser.objects.create_user(
        username='testuser',
        password='testpassword',
        email='test@mail.ru'
    )

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def authenticated_client(api_client, basic_user):
    api_client.force_authenticate(user=basic_user)
    return api_client