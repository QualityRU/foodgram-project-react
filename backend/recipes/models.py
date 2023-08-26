from django.contrib.auth.models import User
from django.db import models


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name='Автор рецепта',
        help_text='Выберите автора рецепта',
        on_delete=models.CASCADE,
        related_name='recipes',
    )
    pub_date = models.DateTimeField(
        verbose_name='Время публикации',
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
        max_length=3000,
    )
    cooking_time = ...

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название тега',
        help_text='Введите название тега',
        unique=True,
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

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название ингредиента',
        help_text='Введите название ингредиента',
        max_length=200
    )
    count = ...
    measurement_unit = models.CharField(
        verbose_name='Единицы измерения',
        help_text='Введите единицу измерения',
        max_length=200
    )

    def __str__(self):
        return self.name
