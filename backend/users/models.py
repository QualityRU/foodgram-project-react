from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator, RegexValidator
from django.db import models


class CustomUser(AbstractUser):
    """Модель кастомного пользователя."""

    email = models.EmailField(
        verbose_name='E-mail',
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
        max_length=150,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
    )
    password = models.CharField(
        verbose_name='Пароль',
        blank=False,
        max_length=150,
    )

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
    """Модель подписок на автора рецепта."""

    follower = models.ForeignKey(
        CustomUser,
        verbose_name='Подписчик',
        on_delete=models.CASCADE,
        related_name='following',
    )
    author = models.ForeignKey(
        CustomUser,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='followers',
    )

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['follower', 'author'], name='unique_follower'
            ),
            models.CheckConstraint(
                check=~models.Q(author=models.F('follower')),
                name='check_author',
            ),
        ]

    def __str__(self):
        return f'{self.follower} подписан на {self.author}'
