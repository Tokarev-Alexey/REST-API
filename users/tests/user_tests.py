import pytest
from django.utils import timezone

from users.models import ProfileUser

"""1. Базовое создание пользователя
Создание пользователя с минимальными данными (username, password)
Создание со всеми полями (email, first_name, last_name и т.д.)
Создание без пароля
Проверка уникальности username

2. Кастомные поля модели
Работа поля subscriptions (ManyToMany к самому себе)
Поле avatar (загрузка, валидация, опциональность)

3. Методы модели
__str__ метод - возвращает username
Стандартные методы Django User модели (get_full_name, etc.)

4. Связи и отношения
Проверка, что пользователь может быть создан без подписок
Проверка работы subscriptions и subscribers

5. Валидация и ограничения
Максимальная длина username (150 символов)
Корректность help_text для username

"""


#Создание пользователя с минимальными данными (username, password)
@pytest.mark.django_db
def test_crete_user_with_password_and_username():
    user = ProfileUser.objects.create_user(username='testuser',
                                           password='testpassword',
                                           )
    assert ProfileUser.objects.filter(username='testuser').exists() #это проверка на наличие в БД
    assert user.id is not None
    assert user.username == 'testuser'
    assert user.check_password('testpassword')


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


#проверка аватара
@pytest.mark.django_db
def test_create_user_avatar():
    user = ProfileUser.objects.create_user(username='testuser',
                                           password='testpassword')
    user.avatar = 'avatars/avatar.jpg'

    assert user.avatar == 'avatars/avatar.jpg'


#проверка подписок
@pytest.mark.django_db
def test_create_user_subscriptions():
    user = ProfileUser.objects.create_user(username='testuser',
                                           password='testpassword',
                                           email=None)
    subscriptions_user = ProfileUser.objects.create_user(username='testsubscriptions',
                                                         password='testpasswordsubscriptions',
                                                         email=None)
    user.subscriptions.add(subscriptions_user)

    assert subscriptions_user in user.subscriptions.all()
    assert user.subscriptions.count() == 1


#ошибка при создании без пароля
@pytest.mark.django_db
def test_create_user_without_password_fails():
    with pytest.raises(ValueError, match="Password is required"):
        ProfileUser.objects.create_user(
            username='testuser',
            email='email.mail.ru'
        )