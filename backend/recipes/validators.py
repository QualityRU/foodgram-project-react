from django.core.exceptions import ValidationError
from rest_framework import serializers
from webcolors import hex_to_name


def validate_colorfield(value):
    try:
        data = hex_to_name(value)
    except ValueError:
        raise ValidationError('Такого цвета нет!')
    return data


class ColorFieldValidator(serializers.Field):
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            data = hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError('Такого цвета нет!')
        return data


class CookingTimeRecipeFieldValidator(serializers.Field):
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            if int(data) <= 0:
                raise serializers.ValidationError(
                    'Время приготовления должно быть больше 0'
                )
        except ValueError:
            raise serializers.ValidationError(
                'Время приготовления должно быть указано цифрой'
            )
        return data


class AmountIngredientFieldValidator(serializers.Field):
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            if int(data) <= 0:
                raise serializers.ValidationError(
                    'Количество ингредиентов не может быть меньше 1'
                )
        except ValueError:
            raise serializers.ValidationError(
                'Количество ингредиентов должно быть указано цифрой'
            )
        return data
