# Generated by Django 4.2.4 on 2023-08-27 07:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='author',
            field=models.ForeignKey(help_text='Выберите автора публикации', on_delete=django.db.models.deletion.CASCADE, related_name='recipe', to=settings.AUTH_USER_MODEL, verbose_name='Автор публикации'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(help_text='Выберите ингриденты', related_name='recipe', through='recipes.IngredientM2MRecipe', to='recipes.ingredient', verbose_name='Ингредиенты'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(help_text='Выберите тег', related_name='recipe', to='recipes.tag', verbose_name='Теги'),
        ),
        migrations.AddField(
            model_name='ingredientm2mrecipe',
            name='ingredient',
            field=models.ForeignKey(help_text='Выберите ингредиент/ы', on_delete=django.db.models.deletion.CASCADE, to='recipes.ingredient', verbose_name='Ингредиент'),
        ),
        migrations.AddField(
            model_name='ingredientm2mrecipe',
            name='recipe',
            field=models.ForeignKey(help_text='Выберите рецепт', on_delete=django.db.models.deletion.CASCADE, related_name='ingredient', to='recipes.recipe', verbose_name='Рецепт'),
        ),
    ]
