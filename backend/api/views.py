from rest_framework import viewsets

from .serializers import (
    CustomUserSerializer,
    IngredientSerializer,
    RecipeSerializer,
    TagSerializer,
)
from recipes.models import Ingredient, Recipe, Tag
from users.models import CustomUser


class CustomUserViewSet(viewsets.ModelViewSet):
    """"""

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """"""

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class TagViewSet(viewsets.ModelViewSet):
    """"""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    """"""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
