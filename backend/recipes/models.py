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
        ordering = [
            ('name'),
        ]

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
        verbose_name='Слаг',
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
        related_name='recipe',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientM2MRecipe',
        related_name='recipe',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        help_text='Выберите тег',
        related_name='recipe',
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
        ordering = ('id',)

    def __str__(self):
        return self.name


class IngredientM2MRecipe(models.Model):
    """Модель для связи моделей Ingredient и Recipe."""

    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='ingredient',
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
        verbose_name = 'ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'

    def __str__(self):
        return f'{self.recipe} - {self.ingredient}, {self.amount}'


class FavoriteRecipe(models.Model):
    """Модель для рецептов, добавленных в избранное."""

    user = models.ForeignKey(
        CustomUser,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='favorite',
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='favorite',
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


class ShoppingCartRecipe(models.Model):
    """Модель для рецептов, добавленных в список покупок."""

    user = models.ForeignKey(
        CustomUser,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='shopping_cart',
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='shopping_cart',
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
