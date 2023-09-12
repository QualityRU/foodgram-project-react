from io import BytesIO

from django.db.models import Sum
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from recipes.models import Ingredient, IngredientAmount


def create_shopping_list_pdf(shopping_cart):
    recipes = shopping_cart.values_list('recipe_id', flat=True)
    buy_list = (
        IngredientAmount.objects.filter(recipe__in=recipes)
        .values('ingredient')
        .annotate(amount=Sum('amount'))
    )

    buffer = BytesIO()
    page = canvas.Canvas(buffer)
    pdfmetrics.registerFont(
        TTFont('Ubuntu-Regular', 'data/fonts/Ubuntu-Regular.ttf', 'UTF-8')
    )
    page.setFont('Ubuntu-Regular', size=20)
    page.drawString(x=130, y=750, text='Список ингредиентов для рецептов')
    page.setFont('Ubuntu-Regular', size=16)
    height = 700

    for item in buy_list:
        i = Ingredient.objects.get(pk=item.get('ingredient'))
        amount = item.get('amount')
        page.drawString(
            x=50,
            y=height,
            text=f'- {i.name} ({i.measurement_unit}) - {amount}',
        )
        height -= 20
    page.showPage()
    page.save()
    pdf = buffer.getvalue()
    buffer.close()
    return pdf
