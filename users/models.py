from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Почта')
    first_name = models.CharField(max_length=150, default='Не указано', verbose_name='Имя', **NULLABLE)
    last_name = models.CharField(max_length=150, default='Не указано', verbose_name='Фамилия', **NULLABLE)
    phone = models.CharField(max_length=35, verbose_name='Телефон', **NULLABLE, default='Не указано')
    city = models.CharField(max_length=50, verbose_name='Город', **NULLABLE, default='Не указано')
    avatar = models.ImageField(upload_to='users/%Y', default='users/non_avatar.png', verbose_name='Аватар', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email
