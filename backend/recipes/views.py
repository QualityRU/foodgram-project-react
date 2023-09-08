from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import IngredientFilter, RecipeFilter
from .models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from .serializers import (
    FavoriteSerializer,
    IngredientSerializer,
    RecipeCreateSerializer,
    RecipeListSerializer,
    ShoppingCartSerializer,
    TagSerializer,
)


class TagViewSet(viewsets.ModelViewSet):
    """Представление для тегов."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ModelViewSet):
    """Представление для ингредиентов."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
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
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_permissions(self):
        """Определение доступа для действия с сериализатором."""
        if self.action in (
            'create',
            'partial_update',
            'favorite',
            'shopping_cart',
        ):
            return [permissions.IsAuthenticated()]
        elif self.action in ('list', 'retrieve'):
            return [permissions.AllowAny()]
        return []

    def get_serializer_class(self):
        """Определение действия с сериализатором."""
        if self.action in ('create', 'partial_update'):
            RecipeCreateSerializer
        elif self.action in ('list', 'retrieve'):
            return RecipeListSerializer
        elif self.action == 'favorite':
            return FavoriteSerializer
        elif self.action == 'shopping_cart':
            return ShoppingCartSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    @action(['POST', 'DELETE'], detail=True)
    def favorite(self, request, pk=None):
        """Добавление и удаление рецептов из избранного."""

        if self.request.method == 'POST':
            serializer = self.get_serializer(
                data=request.data,
                context={'request': request, 'recipe_id': pk},
            )
            serializer.is_valid(raise_exception=True)
            response_data = serializer.save(id=pk)
            return Response(data=response_data, status=status.HTTP_201_CREATED)
        elif self.request.method == 'DELETE':
            user = self.request.user
            recipe = get_object_or_404(Recipe, pk=pk)
            get_object_or_404(Favorite, user=user, recipe=recipe).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(['POST', 'DELETE'], detail=True)
    def shopping_cart(self, request, pk=None):
        """Добавление и удаление рецептов из корзины."""

        if self.request.method == 'POST':
            serializer = self.get_serializer(
                data=request.data,
                context={'request': request, 'recipe_id': pk},
            )
            serializer.is_valid(raise_exception=True)
            response_data = serializer.save(id=pk)
            return Response(data=response_data, status=status.HTTP_201_CREATED)
        elif self.request.method == 'DELETE':
            user = self.request.user
            recipe = get_object_or_404(Recipe, pk=pk)
            get_object_or_404(ShoppingCart, user=user, recipe=recipe).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
