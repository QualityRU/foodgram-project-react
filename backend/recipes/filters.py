import django_filters

from .models import Ingredient, Recipe
from users.models import User


class IngredientFilter(django_filters.FilterSet):
    """Фильтрация ингредиентов по названию."""

    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='istartswith',
    )

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(django_filters.FilterSet):
    """Фильтрация по избранному, автору, списку покупок и тегам."""

    author = django_filters.ModelChoiceFilter(
        field_name='author', queryset=User.objects.all()
    )
    tags = django_filters.AllValuesMultipleFilter(field_name='tags__slug')

    class Meta:
        model = Recipe
        fields = (
            'tags',
            'author',
        )
