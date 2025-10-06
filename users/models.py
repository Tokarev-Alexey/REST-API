from django.db import models
from django.contrib.auth.models import AbstractUser
from project_config.settings import MEDIA_URL

class ProfileUser(AbstractUser):
    '''
    print(ProfileUser.__doc__)  Покажет описание класса
    help(ProfileUser)  Полная справка
    create() - создает запись "как есть", пароль сохраняется в чистом виде и не хеширует пароль.
    create_user() - специальный метод User модели, который хэширует пароль автоматически.
    ProfileUser.objects.create_user(username='test', password='plain_password') НАДО ТАК!
    шобы не забыть
    firstuser = ProfileUser.objects.get(username='firstuser')
    firstuser.subscriptions.add(user) -- firstuser подписался на user
    firstuser.subscribers.add(user) -- -- user подписался на firstuser
    firstuser.subscriptions.all() -- на кого подписан firstuser
    firstuser.subscribers.all() -- подписчики firstuser
    '''
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='username',
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'
    )
    email = models.EmailField(blank=True, unique=True)
    subscriptions = models.ManyToManyField('self', symmetrical=False, related_name='subscribers', blank=True)
    avatar = models.ImageField(upload_to=MEDIA_URL, blank=True, null=True)

    def __str__(self):
        return f'{self.username}'
