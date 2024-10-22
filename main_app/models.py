from django.db import models

from django.contrib.auth.models import AbstractUser


# AbstractUser -> Модель-основа для Джанго юзера
# Ее импортируем тогда, когда хотим "добавить" новые поля
class CustomUser(AbstractUser):
    iin = models.CharField(max_length=12)


from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if email is None:
            raise ValueError('Email is required!')
        email = self.normalize_email(email)
        # self.normalize_email -> Встроенный метод в Джанго, для приведения имейла в порядок
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # set_password -> Сохраняет хэш пароля
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None  # Удаляем поле username из AbstractUser
    email = models.EmailField(unique=True)  # unique=True - Обязателен для полей логинов
    # unique -> Если стоит True, то не дает двум одинаковым значениям оказаться в этом поле

    USERNAME_FIELD = 'email'  # USERNAME_FIELD -> Какое поле используется в качестве логина
    REQUIRED_FIELDS = []  # REQUIRED_FIELDS - > Какие поля обязательны для каждого юзера

    objects = CustomUserManager()  # Привязываем наш новый менеджер к модели


from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    date_joined = models.DateTimeField(auto_now_add=True)
    # auto_now_add -> Автоматически добавляет текущую при создании объекта

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
