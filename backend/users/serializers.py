from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from .models import User
from .validators import UsernameFieldValidator
from recipes.models import Recipe


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

    is_subscribed = serializers.SerializerMethodField(read_only=True)

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

    def get_is_subscribed(self, author):
        user = self.context.get('request').user

        if not self.context.get('request') or user.is_anonymous:
            return False
        return author.subscribe.filter(user=user).exists()


class UserSetPasswordSerializer(serializers.Serializer):
    """Сериализатор для смены пароля."""

    new_password = serializers.CharField(required=True, write_only=True)
    current_password = serializers.CharField(required=True, write_only=True)

    class Meta:
        extra_kwargs = {
            'new_password': {'required': True},
            'current_password': {'required': True},
        }


class RecipeShortShowSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра короткого рецепта."""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        extra_kwargs = {
            'id': {'required': True},
            'name': {'required': True},
            'image': {'required': True},
            'cooking_time': {'required': True},
        }


class SubscriptionSerializer(serializers.Serializer):
    """Сериализатор для просмотра подписок пользователя."""

    is_subscribed = serializers.SerializerMethodField(read_only=True)
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)

    def get_is_subscribed(self, author):
        if not self.context.get('request'):
            return False
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return author.subscribe.filter(user=user).exists()

    def get_recipes(self, author):
        request = self.context.get('request')
        if not request:
            return False
        user = self.context.get('request').user
        if user.is_anonymous:
            return False

        recipes = author.recipes.filter(author=author)
        recipes_limit = request.query_params.get('recipes_limit')

        if recipes_limit:
            recipes = recipes[: int(recipes_limit)]
        else:
            recipes = recipes.all()
        return RecipeShortShowSerializer(
            instance=recipes, many=True, context={'request': request}
        ).data

    def get_recipes_count(self, author):
        return author.recipes.count()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )
        extra_kwargs = {
            'email': {'required': True},
            'id': {'required': True},
            'username': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'is_subscribed': {'required': True},
            'recipes': {'required': True},
            'recipes_count': {'required': True},
        }


class SubscribeSerializer(serializers.Serializer):
    """Добавление и удаление подписок пользователя."""

    def validate(self, data):
        user = self.context.get('request').user
        author = get_object_or_404(User, pk=self.context.get('id'))
        if user == author:
            raise serializers.ValidationError(
                'Вы не можете подписаться на себя самого'
            )
        if author.subscribe.filter(user=user).exists():
            raise serializers.ValidationError(
                'Вы уже подписаны на этого пользователя'
            )
        return data

    def create(self, validated_data):
        user = self.context.get('request').user
        author = get_object_or_404(User, pk=validated_data['id'])
        author.subscribe.create(user=user)
        return SubscriptionSerializer(
            author, context={'request': self.context.get('request')}
        ).data
