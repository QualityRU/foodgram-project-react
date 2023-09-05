from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets

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


class IngredientViewSet(viewsets.ModelViewSet):
    """Представление для ингредиентов."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (DjangoFilterBackend,)


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

    def get_permissions(self):
        """Определение доступа для действия с сериализатором."""
        if self.action == 'create':
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticated(),)

    def get_serializer_class(self):
        """Определение действия с сериализатором."""
        if self.action in ('list', 'retrieve'):
            return RecipeGetSerializer
