from django.db import models

from users.models import CustomUser


class Recipe(models.Model):
    """Модель рецептов."""

    author = models.ForeignKey(
        CustomUser,
        verbose_name='Автор рецепта',
        help_text='Выберите автора рецепта',
        on_delete=models.CASCADE,
        related_name='recipe',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )
    ingredients = ...
    tags = ...
    image = ...
    name = models.CharField(
        verbose_name='Название рецепта',
        help_text='Введите название рецепта',
        max_length=200,
    )
    text = models.TextField(
        verbose_name='Описание рецепта',
        help_text='Введите описание рецепта',
    )
    cooking_time = ...

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Модель тегов."""

    name = models.CharField(
        verbose_name='Название тега',
        help_text='Введите название тега',
        unique=True,
        db_index=True,
        max_length=200,
    )
    color = models.CharField(
        verbose_name='Цвет',
        help_text='Введите цвет тега',
        unique=True,
        max_length=7,
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        help_text='Введите слаг тега',
        unique=True,
        max_length=200,
    )

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель ингредиентов."""

    name = models.CharField(
        verbose_name='Название ингредиента',
        help_text='Введите название ингредиента',
        unique=True,
        db_index=True,
        max_length=200,
    )
    count = ...
    measurement_unit = models.CharField(
        verbose_name='Единицы измерения',
        help_text='Введите единицу измерения',
        max_length=200,
    )

    class Meta:
        verbose_name = 'ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name
