from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets

from .models import Ingredient, Recipe, Tag
from .serializers import IngredientSerializer, RecipeSerializer, TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """Представление для рецептов."""

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    # permission_classes = (permissions.IsOwnerOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)


class TagViewSet(viewsets.ModelViewSet):
    """Представление для тегов."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    # permission_classes = (permissions.AllowAny,)


class IngredientViewSet(viewsets.ModelViewSet):
    """Представление для ингредиентов."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    # permission_classes = (permissions.AllowAny,)
    filter_backends = (DjangoFilterBackend,)
