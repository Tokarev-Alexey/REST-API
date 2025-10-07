from django.contrib.auth.models import UserManager


class ProfileUserManager(UserManager):
    """Причина создания:
        Кастомизация процесса создания пользователей с обязательной проверкой пароля и особой логикой для email.

        Ключевые отличия от стандартного UserManager:
        - Пароль обязателен (стандартный менеджер позволяет создавать пользователей без пароля)
        - Email нормализуется в None если пустой (стандартный менеджер оставляет пустую строку)
        - create_superuser явно проверяет наличие пароля перед созданием

        Цель: Гарантировать что все пользователи в системе имеют пароль и корректно обработанный email."""

    def create_user(self, username, email=None, password=None, **extra_fields):
        if not password:
            raise ValueError("Требуется ввести пароль.")

        if not username:
            raise ValueError('Необходимо указать имя пользователя.')

        if self.model.objects.filter(username=username).exists():
            raise ValueError("Пользователь с таким именем уже есть.")

        if email == '' or email is None:
            email = None
        else:
            email = self.normalize_email(email)

        if self.model.objects.filter(email=email).exists():
            raise ValueError("Этот email уже зарегистрирован.")

        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        if not password:
            raise ValueError("Требуется ввести пароль.")

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь статус is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь статус is_superuser=True.')

        # 4. Вызов create_user с установленными флагами
        return self.create_user(username, email, password, **extra_fields)