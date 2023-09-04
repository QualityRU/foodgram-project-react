from rest_framework import serializers

from .models import Ingredient, Recipe, Tag
from .validators import ColorFieldValidator


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для рецептов."""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тегов."""

    color = ColorFieldValidator()

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для ингридентов."""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')
