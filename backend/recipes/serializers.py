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


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для ингридентов."""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipeGetSerializer(serializers.ModelSerializer):
    """Сериализатор для рецептов."""

    tags = TagSerializer(many=True, read_only=True)
    author = UserReadSerializer(
        default=serializers.CurrentUserDefault(), read_only=True
    )
    ingredients = IngredientSerializer(many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField(required=True)

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
