import pytest
from users.models import ProfileUser
from posts.models import Post, Comment
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

@pytest.fixture()
def basic_post(basic_user):
    return Post.objects.create(title='Заголовок',
                               text='Какой-то текст поста.',
                               author=basic_user)

@pytest.fixture()
def basic_comment(basic_user, basic_post):
    return Comment.objects.create(post=basic_post,
                                  author_comm=basic_user,
                                  text_comm='Комментарий')

@pytest.fixture()
def fabric_posts():
    def create(**kwargs):
        return Post.objects.create(**kwargs)
    return create

@pytest.fixture()
def fabric_users():
    def create(**kwargs):
        return ProfileUser.objects.create(**kwargs)
    return create