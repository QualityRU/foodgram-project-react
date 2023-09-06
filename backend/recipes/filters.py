import django_filters

from .models import Ingredient


class IngredientFilter(django_filters.FilterSet):
    """Фильтрация ингредиентов по названию."""

    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='istartswith',
    )

    class Meta:
        model = Ingredient
        fields = ('name',)
