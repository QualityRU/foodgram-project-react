from django.contrib import admin

from .models import Ingredient, IngredientM2MRecipe, Recipe, Tag


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    ...


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    ...


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    ...


@admin.register(IngredientM2MRecipe)
class IngredientM2MRecipe(admin.ModelAdmin):
    ...
