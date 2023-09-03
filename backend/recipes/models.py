from django.core.validators import MinValueValidator
from django.db import models

from .validators import ColorFieldValidator
from users.models import CustomUser


class Ingredient(models.Model):
    """Модель ингредиентов."""

    name = models.CharField(
        verbose_name='Название',
        db_index=True,
        blank=False,
        max_length=200,
    )
    measurement_unit = models.CharField(
        verbose_name='Единицы измерения',
        blank=False,
        max_length=20,
    )

    class Meta:
        verbose_name = 'ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Модель тегов."""

    name = models.CharField(
        verbose_name='Название',
        unique=True,
        db_index=True,
        blank=False,
        max_length=200,
    )
    color = models.CharField(
        verbose_name='Цвет',
        unique=True,
        blank=False,
        max_length=7,
        validators=[ColorFieldValidator],
    )
    slug = models.SlugField(
        verbose_name='Индентификатор',
        unique=True,
        blank=False,
        max_length=200,
    )

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецептов."""

    author = models.ForeignKey(
        CustomUser,
        verbose_name='Автор публикации',
        on_delete=models.CASCADE,
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientAmount',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
    )
    image = models.ImageField(
        verbose_name='Фотограция',
        upload_to='recipes/',
    )
    name = models.CharField(
        verbose_name='Название',
        blank=False,
        max_length=200,
    )
    text = models.TextField(
        verbose_name='Текстовое описание',
        blank=False,
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления в минутах',
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
        ordering = ('name',)

    def __str__(self):
        return self.name


class IngredientAmount(models.Model):
    """Модель количества ингредиентов."""

    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        on_delete=models.CASCADE,
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=[
            MinValueValidator(
                limit_value=1, message='Ингредиентов не может быть меньше 1!'
            )
        ],
    )

    class Meta:
        verbose_name = 'количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'
        ordering = ('recipe',)

    def __str__(self):
        return f'{self.recipe} - {self.ingredient}, {self.amount}'


class Favorite(models.Model):
    """Модель для избранных рецептов."""

    user = models.ForeignKey(
        CustomUser,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'избранный'
        verbose_name_plural = 'Избранные'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'], name='favorite_unique'
            )
        ]

    def __str__(self):
        return f'{self.user} добавил {self.recipe} в избранное'


class ShoppingCart(models.Model):
    """Модель для рецептов в корзины."""

    user = models.ForeignKey(
        CustomUser,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'корзина'
        verbose_name_plural = 'Корзины'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'], name='shopping_cart_unique'
            )
        ]

    def __str__(self):
        return f'{self.user} добавил {self.recipe} в корзину'
