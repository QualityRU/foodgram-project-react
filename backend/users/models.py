from django.contrib.auth.models import AbstractUser, Group
from django.core.validators import EmailValidator, RegexValidator
from django.db import models


class CustomGroup(Group):
    class Meta:
        verbose_name = 'доступ'
        verbose_name_plural = 'Доступы'


class CustomUser(AbstractUser):
    email = models.EmailField(
        verbose_name='E-mail',
        help_text='Введите e-mail',
        unique=True,
        blank=False,
        max_length=254,
        validators=[
            EmailValidator(
                message='e-mail не прошел валидацию!',
            ),
        ],
    )
    username = models.CharField(
        verbose_name='Username',
        help_text='Введите username',
        unique=True,
        blank=False,
        max_length=150,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+\z',
                message='username не прошел валидацию!',
            ),
        ],
        error_messages={
            'unique': 'Пользователь с таким username уже создан!',
        },
    )
    first_name = models.CharField(
        verbose_name='Имя',
        help_text='Введите имя',
        max_length=150,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        help_text='Введите фамилию',
        max_length=150,
    )
    password = models.CharField(
        verbose_name='Пароль',
        help_text='Введите пароль',
        blank=False,
        max_length=150,
    )

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email
