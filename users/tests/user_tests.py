import pytest
from django.utils import timezone
from users.models import ProfileUser
from conftest import basic_user

"""1. Базовое создание пользователя
Создание пользователя с минимальными данными (username, password)
Создание со всеми полями (email, first_name, last_name и т.д.)
Создание без пароля
проверка custom fields добавления аватара
проверка custom fields создания подписок
Проверка уникальности username
Проверка уникальности email

2. Кастомные поля модели
Работа поля subscriptions (ManyToMany к самому себе)
Поле avatar (загрузка, валидация, опциональность)

3. Методы модели
__str__ метод - возвращает username
"""

# Маркируем все тесты в файле
pytestmark = pytest.mark.users


# Создание пользователя с минимальными данными (username, password)
@pytest.mark.django_db
def test_crete_user_with_password_and_username(basic_user):
    assert ProfileUser.objects.filter(username='testuser').exists() #это проверка на наличие в БД
    assert basic_user.id is not None
    assert basic_user.username == 'testuser'
    assert basic_user.check_password('testpassword')


# Создание со всеми полями (email, first_name, last_name и т.д.)
@pytest.mark.django_db
def test_create_user_with_fullinfo():
    user = ProfileUser.objects.create_user(username='testuser',
                                           password='testpassword',
                                           email='mail@mail.ru',
                                           first_name='Leha',
                                           last_name = 'Batkovich',
                                           is_active = True,
                                           is_staff = False,
                                           is_superuser = False,
                                           date_joined=timezone.now()
                                           )
    assert user.username == 'testuser'
    assert user.check_password('testpassword')
    assert user.email == 'mail@mail.ru'
    assert user.first_name == 'Leha'
    assert user.last_name == 'Batkovich'
    assert user.is_active is True
    assert user.is_staff is False
    assert user.is_superuser is False
    assert user.date_joined is not None  # дата установлена


# Создание без пароля.
@pytest.mark.django_db
def test_create_user_without_password_fails():
    with pytest.raises(ValueError, match="Требуется ввести пароль"):
        ProfileUser.objects.create_user(
            username='testuser',
            email='email.mail.ru'
        )


#проверка custom fields добавления аватара
@pytest.mark.django_db
def test_create_user_avatar(basic_user):
    basic_user.avatar = 'avatars/avatar.jpg'

    assert basic_user.avatar == 'avatars/avatar.jpg'


#проверка custom fields создания подписок
@pytest.mark.django_db
def test_create_user_subscriptions(basic_user):
    subscriptions_user = ProfileUser.objects.create_user(username='testsubscriptions',
                                                         password='testpasswordsubscriptions',
                                                         email=None)
    basic_user.subscriptions.add(subscriptions_user)

    assert subscriptions_user in basic_user.subscriptions.all()
    assert basic_user.subscriptions.count() == 1


# проверка уникальности username
@pytest.mark.django_db
def test_uniq_username(basic_user):
    with pytest.raises(ValueError, match="Пользователь с таким именем уже есть"):
        ProfileUser.objects.create_user(
            username='testuser',  # То же имя
            password='pass',
            email='email.mail.ru'
        )


# проверка уникальности email
@pytest.mark.django_db
def test_uniq_email(basic_user):
    with pytest.raises(ValueError, match="Этот email уже зарегистрирован."):
        ProfileUser.objects.create_user(
            username='user',
            password='pass',
            email='test@mail.ru'
        )

# __str__ метод - возвращает username
@pytest.mark.django_db
def test_str(basic_user):
    assert basic_user.__str__() == basic_user.username