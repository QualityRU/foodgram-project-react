from django.core.validators import MinValueValidator
from django.db import models

from users.models import CustomUser


class Ingredient(models.Model):
    """Модель ингредиентов."""

    name = models.CharField(
        verbose_name='Название',
        help_text='Введите название',
        unique=True,
        db_index=True,
        blank=False,
        max_length=200,
    )
    measurement_unit = models.CharField(
        verbose_name='Единицы измерения',
        help_text='Введите единицу измерения',
        blank=False,
        max_length=200,
    )

    class Meta:
        verbose_name = 'ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Модель тегов."""

    name = models.CharField(
        verbose_name='Название',
        help_text='Введите название',
        unique=True,
        db_index=True,
        blank=False,
        max_length=200,
    )
    color = models.CharField(
        verbose_name='Цвет',
        help_text='Введите цвет',
        unique=True,
        blank=False,
        max_length=7,
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        help_text='Введите слаг',
        unique=True,
        blank=False,
        max_length=200,
    )

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецептов."""

    author = models.ForeignKey(
        CustomUser,
        verbose_name='Автор публикации',
        help_text='Выберите автора публикации',
        on_delete=models.CASCADE,
        related_name='recipe',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты',
        help_text='Выберите ингриденты',
        through='IngredientM2MRecipe',
        related_name='recipe',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        help_text='Выберите тег',
        related_name='recipe',
    )
    image = ...
    name = models.CharField(
        verbose_name='Название',
        help_text='Введите название',
        blank=False,
        max_length=200,
    )
    text = models.TextField(
        verbose_name='Текстовое описание',
        help_text='Введите текстовое описание',
        blank=False,
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления в минутах',
        help_text='Введите время приготовления в минутах',
        blank=False,
        validators=[
            MinValueValidator(
                limit_value=1,
                message='Время приготовления не может быть меньше 1 минуты!',
            )
        ],
    )

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientM2MRecipe(models.Model):
    """Модель для связи моделей Ingredient и Recipe."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient',
        verbose_name='Рецепт',
        help_text='Выберите рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        help_text='Выберите ингредиент/ы',
        on_delete=models.CASCADE,
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        help_text='Введите количество',
        validators=[
            MinValueValidator(
                limit_value=1, message='Ингредиентов не может быть меньше 1!'
            )
        ],
    )

    class Meta:
        verbose_name = 'ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'
