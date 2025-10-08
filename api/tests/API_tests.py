import pytest
from conftest import *
from posts.models import *

pytestmark = pytest.mark.api

@pytest.mark.django_db
def test_get_comment(api_client, comment):
    response = api_client.get('/comment/')
    assert response.status_code == 200
    assert Comment.objects.count() == 1

@pytest.mark.django_db
def test_create_comment(authenticated_client, post):
    response = authenticated_client.post('/comment/', {
        'post': post.id,
        'text_comm': 'Комментарий'
    })
    assert response.status_code == 201
    assert Comment.objects.count() == 1

@pytest.mark.django_db
def test_create_comment_no_auth(api_client, post):
    response = api_client.post('/comment/', {
        'post': post.id,
        'text_comm': 'Комментарий'
    })
    assert response.status_code == 401 or response.status_code == 403

@pytest.mark.django_db
def test_del_comment(authenticated_client,comment):
    response = authenticated_client.delete('/comment/1/')
    assert response.status_code == 204
    assert Comment.objects.count() == 0

@pytest.mark.django_db
def test_del_comment_no_auth(api_client,comment):
    response = api_client.delete('/comment/1/')
    assert response.status_code == 401 or response.status_code == 403

@pytest.mark.django_db
def test_feed_content(authenticated_client, fabric_posts,fabric_users, basic_user):
    Jon = fabric_users(username='Jon', password='pass', email='a@mail.ru')
    Anna = fabric_users(username='Anna', password='pass', email='b@mail.ru')
    Ben = fabric_users(username='Ben', password='pass', email='d@mail.ru')

    post_jon = fabric_posts(title='пост Джона', text='текст', author=Jon)
    post_anna = fabric_posts(title='пост Анны', text='текст', author=Anna)
    post_ben = fabric_posts(title='пост Бена', text='текст', author=Ben)

    basic_user.subscriptions.add(Jon)
    basic_user.subscriptions.add(Anna)

    response = authenticated_client.get('/post/posts_from_subscriptions/')
    post_titles = [post['title'] for post in response.data]
    assert response.status_code == 200
    assert len(response.data) == 2
    assert 'пост Джона' in post_titles
