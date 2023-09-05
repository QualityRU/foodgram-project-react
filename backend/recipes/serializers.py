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
        extra_kwargs = {
            'id': {'required': True},
            'name': {'required': True},
            'color': {'required': True},
            'slug': {'required': True},
        }


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для ингридентов."""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')
        extra_kwargs = {
            'id': {'required': True},
            'name': {'required': True},
            'measurement_unit': {'required': True},
        }


class RecipeShortShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        extra_kwargs = {
            'id': {'required': True},
            'name': {'required': True},
            'image': {'required': True},
            'cooking_time': {'required': True},
        }
