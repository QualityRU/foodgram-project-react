from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from .models import CustomUser, Follow


class UserCreateSerializer(UserCreateSerializer):
    """"""

    class Meta(UserCreateSerializer.Meta):
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
        )


class UserReadSerializer(UserSerializer):
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

        if request and request.user.is_authenticated:
            return Follow.objects.filter(
                follower=request.user, author=obj
            ).exists()
        return False
