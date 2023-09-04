from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from .models import User, Follow
from .validators import UsernameFieldValidator


class UserCreateSerializer(UserCreateSerializer):
    """Сериализатор для регистрации пользоваля."""

    username = UsernameFieldValidator()

    class Meta(UserCreateSerializer.Meta):
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
        )
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'password': {'required': True},
        }


class UserReadSerializer(UserSerializer):
    """Сериализатор для чтения полей пользователя."""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')

        if not request or request.user.is_anonymous:
            return False

        return Follow.objects.filter(
            follower=request.user, author=obj
        ).exists()


class UserSetPasswordSerializer(serializers.Serializer):
    """Сериализатор для смены пароля."""

    new_password = serializers.CharField(required=True, write_only=True)
    current_password = serializers.CharField(required=True, write_only=True)

    class Meta:
        extra_kwargs = {
            'new_password': {'required': True},
            'current_password': {'required': True},
        }
