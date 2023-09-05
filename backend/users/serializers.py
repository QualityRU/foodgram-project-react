from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from .models import Subscribe, User
from .validators import UsernameFieldValidator
from recipes.models import Recipe
from recipes.serializers import RecipeShortShowSerializer


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
        request = self.context.get('request')

        if not request or request.user.is_anonymous:
            return False
        return author.following.filter(user=request.user).exists()


class UserSetPasswordSerializer(serializers.Serializer):
    """Сериализатор для смены пароля."""

    new_password = serializers.CharField(required=True, write_only=True)
    current_password = serializers.CharField(required=True, write_only=True)

    class Meta:
        extra_kwargs = {
            'new_password': {'required': True},
            'current_password': {'required': True},
        }


class SubscriptionSerializer(serializers.Serializer):
    """Сериализатор для просмотра подписок пользователя."""

    is_subscribed = serializers.SerializerMethodField(read_only=True)
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)

    def get_is_subscribed(self, author):
        request = self.context.get('request')

        if not request or request.user.is_anonymous:
            return False
        return author.following.filter(user=request.user).exists()

    def get_recipes(self, author):
        request = self.context.get('request')

        if not request or request.user.is_anonymous:
            return False

        recipes = Recipe.objects.filter(author=author)
        recipes_limit = request.query_params.get('recipes_limit')

        if recipes_limit:
            recipes = recipes[: int(recipes_limit)]
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
