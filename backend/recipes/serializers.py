from django.shortcuts import get_object_or_404
from drf_base64.fields import Base64ImageField
from rest_framework import serializers

from .models import Ingredient, Recipe, Tag
from .validators import ColorFieldValidator
from users.serializers import UserListSerializer


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


class RecipeListSerializer(serializers.ModelSerializer):
    """Сериализатор для рецептов."""

    tags = TagSerializer(many=True, read_only=True)
    author = UserListSerializer(
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
        user = self.context.get('request').user
        return recipe.favorite.filter(user=user).exists()

    def get_is_in_shopping_cart(self, recipe):
        user = self.context.get('request').user
        return recipe.shoppingcart.filter(user=user).exists()


class RecipeListShortSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра короткого рецепта."""

    image = Base64ImageField(required=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для cоздания и обновления рецептов."""


class FavoriteSerializer(serializers.Serializer):
    """Сериализатор для добавления и удаления из избранных рецептов."""

    def validate(self, data):
        user = self.context.get('request').user
        recipe_id = self.context.get('recipe_id')
        if user.favorite.filter(recipe_id=recipe_id).exists():
            raise serializers.ValidationError(
                'Вы уже добавили этот рецепт в избранное'
            )
        return data

    def create(self, validated_data):
        user = self.context.get('request').user
        recipe = get_object_or_404(Recipe, pk=validated_data.get('id'))
        recipe.favorite.create(user=user)
        return RecipeListShortSerializer(
            instance=recipe, context={'request': self.context.get('request')}
        ).data


class ShoppingCartSerializer(serializers.Serializer):
    """Сериализатор для добавления и удаления рецептов из корзины покупок."""

    def validate(self, data):
        user = self.context.get('request').user
        recipe_id = self.context.get('recipe_id')
        if user.shoppingcart.filter(recipe_id=recipe_id).exists():
            raise serializers.ValidationError(
                'Вы уже добавили этот рецепт в список покупок'
            )
        return data

    def create(self, validated_data):
        user = self.context.get('request').user
        recipe = get_object_or_404(Recipe, pk=validated_data.get('id'))
        recipe.shoppingcart.create(user=user)
        return RecipeListShortSerializer(
            instance=recipe, context={'request': self.context.get('request')}
        ).data
