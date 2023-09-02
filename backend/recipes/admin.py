from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export.resources import ModelResource

from .models import (
    FavoriteRecipe,
    Ingredient,
    IngredientM2MRecipe,
    Recipe,
    ShoppingCartRecipe,
    Tag,
)


class RecipeResource(ModelResource):
    """Модель ресурсов рецептов."""

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'author',
            'pub_date',
        )


class IngredientsInline(admin.TabularInline):
    model = IngredientM2MRecipe
    extra = 0
    min_num = 1


@admin.register(Recipe)
class RecipeAdmin(ImportExportModelAdmin):
    """Регистрация модели рецептов и импорта/эскпорта в админ-панели."""

    resource_class = (RecipeResource,)
    inlines = (IngredientsInline,)
    list_display = (
        'id',
        'name',
        'author',
        'pub_date',
    )
    list_filter = ('author', 'name', 'tags')
    search_fields = ('name', 'author')


class TagResource(ModelResource):
    """Модель ресурсов тегов."""

    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )


@admin.register(Tag)
class TagAdmin(ImportExportModelAdmin):
    """Регистрация модели тегов и импорта/эскпорта в админ-панели."""

    resource_class = (TagResource,)
    list_display = (
        'id',
        'name',
        'color',
        'slug',
    )
    search_fields = ('name', 'color', 'slug')


class IngredientResource(ModelResource):
    """Модель ресурсов ингредиентов."""

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )


@admin.register(Ingredient)
class IngredientAdmin(ImportExportModelAdmin):
    """Регистрация модели ингредиентов и импорта/эскпорта в админ-панели."""

    resource_classes = (IngredientResource,)
    list_display = (
        'id',
        'name',
        'measurement_unit',
    )


class IngredientM2MRecipeResource(ModelResource):
    """Модель ингредиента в рецепте."""

    class Meta:
        model = IngredientM2MRecipe
        fields = (
            'id',
            'recipe',
            'ingredient',
            'amount',
        )


@admin.register(IngredientM2MRecipe)
class IngredientM2MRecipeAdmin(ImportExportModelAdmin):
    """
    Регистрация модели ингредиентов в рецепте и
    импорта/эскпорта в админ-панели.
    """

    resource_classes = (IngredientM2MRecipeResource,)
    list_display = (
        'id',
        'recipe',
        'ingredient',
        'amount',
    )
    search_fields = ('recipe', 'ingredient')


class FavoriteRecipeResource(ModelResource):
    """Модель ресурсов избранных рецептов."""

    class Meta:
        model = FavoriteRecipe
        fields = (
            'id',
            'user',
            'recipe',
        )


@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(ImportExportModelAdmin):
    """
    Регистрация модели избранных рецептов и импорта/эскпорта в админ-панели.
    """

    resource_classes = (FavoriteRecipeResource,)
    list_display = (
        'id',
        'user',
        'recipe',
    )
    search_fields = ('user', 'recipe')


class ShoppingCartRecipeResource(ModelResource):
    """Модель ресурсов рецептов в корзине."""

    class Meta:
        model = ShoppingCartRecipe
        fields = (
            'id',
            'user',
            'recipe',
        )


@admin.register(ShoppingCartRecipe)
class ShoppingCartRecipeAdmin(ImportExportModelAdmin):
    """
    Регистрация модели рецептов в корзине и импорта/эскпорта в админ-панели.
    """

    resource_classes = (ShoppingCartRecipeResource,)
    list_display = (
        'id',
        'user',
        'recipe',
    )
    search_fields = ('user', 'recipe')
