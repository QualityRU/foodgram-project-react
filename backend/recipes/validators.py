from django.core.exceptions import ValidationError
from rest_framework import serializers
from webcolors import hex_to_name


def ColorFieldValidator(value):
    try:
        data = hex_to_name(value)
    except ValueError:
        raise ValidationError('Такого цвета нет!')
    return data


class ColorSerializerValidator(serializers.Field):
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            data = hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError('Такого цвета нет!')
        return data
