from rest_framework import serializers

from recipes.models import Ingredient, Recipe, Tag
from users.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    """"""

    class Meta:
        model = CustomUser
        fields = '__all__'


class RecipeSerializer(serializers.ModelSerializer):
    """"""

    class Meta:
        model = Recipe
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    """"""

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    """"""

    class Meta:
        model = Ingredient
        fields = '__all__'
