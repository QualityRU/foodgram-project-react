# Generated by Django 4.2.4 on 2023-08-26 08:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, help_text='Введите название ингредиента', max_length=200, unique=True, verbose_name='Название ингредиента')),
                ('measurement_unit', models.CharField(help_text='Введите единицу измерения', max_length=200, verbose_name='Единицы измерения')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, help_text='Введите название тега', max_length=200, unique=True, verbose_name='Название тега')),
                ('color', models.CharField(help_text='Введите цвет тега', max_length=7, unique=True, verbose_name='Цвет')),
                ('slug', models.SlugField(help_text='Введите слаг тега', max_length=200, unique=True, verbose_name='Слаг')),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('name', models.CharField(help_text='Введите название рецепта', max_length=200, verbose_name='Название рецепта')),
                ('text', models.TextField(help_text='Введите описание рецепта', max_length=3000, verbose_name='Описание рецепта')),
                ('author', models.ForeignKey(help_text='Выберите автора рецепта', on_delete=django.db.models.deletion.CASCADE, related_name='recipe', to=settings.AUTH_USER_MODEL, verbose_name='Автор рецепта')),
            ],
        ),
    ]