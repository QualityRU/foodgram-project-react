from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator, RegexValidator
from django.db import models
from rest_framework.authtoken.models import Token


class CustomToken(Token):
    """Модель токенов пользователя."""

    class Meta:
        verbose_name = 'токен'
        verbose_name_plural = 'Токены'


class CustomUser(AbstractUser):
    """Модель пользователя."""

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
        # validators=[
        #     RegexValidator(
        #         regex=r'^[\w.@+-]+\z',
        #         message='username не прошел валидацию!',
        #     ),
        # ],
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

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = [
        'email',
        'first_name',
        'last_name',
        'password',
    ]

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['email']
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'], name='unique_user'
            )
        ]

    def __str__(self):
        return f'{self.username} ({self.email})'


class Follow(models.Model):
    """Модель подписок на автора."""

    follower = models.ForeignKey(
        CustomUser,
        verbose_name='Подписчик',
        help_text='Введите подписчика',
        on_delete=models.CASCADE,
        related_name='following',
    )
    author = models.ForeignKey(
        CustomUser,
        verbose_name='Автор',
        help_text='Введите автора',
        on_delete=models.CASCADE,
        related_name='followers',
    )

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.follower} подписан на {self.author}'
