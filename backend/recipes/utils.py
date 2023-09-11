from django.db.models import Sum

from recipes.models import Ingredient, IngredientAmount


def create_shopping_list(shopping_cart):
    recipes = shopping_cart.values_list('recipe_id', flat=True)
    buy_list = (
        IngredientAmount.objects.filter(recipe__in=recipes)
        .values('ingredient')
        .annotate(amount=Sum('amount'))
    )
    buy_list_text = 'Список покупок:\n'

    for item in buy_list:
        ingredient = Ingredient.objects.get(pk=item.get('ingredient'))
        amount = item.get('amount')
        buy_list_text += (
            f'{ingredient.name}, {amount} {ingredient.measurement_unit}\n'
        )
    return buy_list_text
