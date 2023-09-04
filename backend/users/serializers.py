from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from .models import CustomUser, Follow
from .validators import UsernameFieldValidator


class CustomUserCreateSerializer(UserCreateSerializer):
    """"""

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


class CustomUserReadSerializer(UserSerializer):
    """"""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
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
