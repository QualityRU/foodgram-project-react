from drf_base64.fields import Base64ImageField
from rest_framework import serializers

from .models import Ingredient, Recipe, Tag
from .validators import ColorFieldValidator
from users.serializers import UserReadSerializer


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


class RecipeGetSerializer(serializers.ModelSerializer):
    """Сериализатор для рецептов."""

    tags = TagSerializer(many=True, read_only=True)
    author = UserReadSerializer(
        default=serializers.CurrentUserDefault(), read_only=True
    )
    ingredients = IngredientSerializer(many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )
        extra_kwargs = {
            'id': {'required': True},
            'tags': {'required': True},
            'author': {'required': True},
            'ingredients': {'required': True},
            'is_favorited': {'required': True},
            'is_in_shopping_cart': {'required': True},
            'name': {'required': True},
            'image': {'required': True},
            'text': {'required': True},
            'cooking_time': {'required': True},
        }

    def get_is_favorited(self, recipe):
        if not self.context.get('request'):
            return False
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return recipe.favorite.filter(user=user).exists()

    def get_is_in_shopping_cart(self, recipe):
        if not self.context.get('request'):
            return False
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return recipe.shoppingcart.filter(user=user).exists()
