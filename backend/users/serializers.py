from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_base64.fields import Base64ImageField
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


class UserListSerializer(UserSerializer):
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

    def get_is_subscribed(self, author):
        user = self.context.get('request').user
        return author.subscribed.filter(user=user).exists()


class UserSetPasswordSerializer(serializers.Serializer):
    """Сериализатор для смены пароля."""

    new_password = serializers.CharField(required=True, write_only=True)
    current_password = serializers.CharField(required=True, write_only=True)


class RecipeListShortSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра короткого рецепта."""

    image = Base64ImageField(required=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscriptionSerializer(serializers.Serializer):
    """Сериализатор для просмотра подписок пользователя."""

    email = serializers.EmailField()
    id = serializers.IntegerField()
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    def get_is_subscribed(self, author):
        user = self.context.get('request').user
        return author.subscribed.filter(user=user).exists()

    def get_recipes(self, author):
        request = self.context.get('request')
        recipes = author.recipes.filter(author=author)
        recipes_limit = request.query_params.get('recipes_limit')

        if recipes_limit:
            recipes = recipes[: int(recipes_limit)]
        else:
            recipes = recipes.all()
        return RecipeListShortSerializer(
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


class SubscribeSerializer(serializers.Serializer):
    """Сериализатор для добавления и удаления подписок пользователя."""

    def validate(self, data):
        user = self.context.get('request').user
        author = get_object_or_404(User, pk=self.context.get('id'))
        if user == author:
            raise serializers.ValidationError(
                'Вы не можете подписаться на себя самого'
            )
        if author.subscribed.filter(user=user).exists():
            raise serializers.ValidationError(
                'Вы уже подписаны на этого пользователя'
            )
        return data

    def create(self, validated_data):
        user = self.context.get('request').user
        author = get_object_or_404(User, pk=validated_data.get('id'))
        author.subscribed.create(user=user)
        return SubscriptionSerializer(
            instance=author, context={'request': self.context.get('request')}
        ).data
