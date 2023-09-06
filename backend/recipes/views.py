from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets

from .filters import IngredientFilter
from .models import Ingredient, Recipe, Tag
from .serializers import (
    IngredientSerializer,
    RecipeGetSerializer,
    TagSerializer,
)


class TagViewSet(viewsets.ModelViewSet):
    """Представление для тегов."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = None


class IngredientViewSet(viewsets.ModelViewSet):
    """Представление для ингредиентов."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    """Представление для рецептов."""

    queryset = Recipe.objects.all()
    http_method_names = [
        'get',
        'post',
        'patch',
        'delete',
    ]
    serializer_class = RecipeGetSerializer
    filter_backends = (DjangoFilterBackend,)

    def get_serializer_class(self):
        """Определение действия с сериализатором."""
        if self.action in ('list', 'retrieve'):
            return RecipeGetSerializer
