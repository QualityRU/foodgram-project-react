from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import User
from .serializers import (
    SubscriptionSerializer,
    UserCreateSerializer,
    UserReadSerializer,
    UserSetPasswordSerializer,
)


class UserViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """Представление пользователя."""

    queryset = User.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('email', 'username')
    filterset_fields = ('email', 'username')

    def get_permissions(self):
        """Определение доступа для действия с сериализатором."""
        if self.action == 'create':
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticated(),)

    def get_serializer_class(self):
        """Определение действия с сериализатором."""
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action == 'set_password':
            return UserSetPasswordSerializer
        elif self.action in ('list', 'retrieve', 'me'):
            return UserReadSerializer
        elif self.action == 'subscriptions':
            return SubscriptionSerializer

    @action(['GET'], detail=False)
    def me(self, request):
        """Текущий пользователь."""
        serializer = self.get_serializer(request.user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(['POST'], detail=False)
    def set_password(self, request):
        """Изменение пароля пользователя."""
        user = request.user
        serializer = self.get_serializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        new_password = serializer.validated_data.get('new_password')
        old_password = serializer.validated_data.get('current_password')

        if not user.check_password(old_password):
            return Response(
                data='Неверный пароль', status=status.HTTP_400_BAD_REQUEST
            )
        if new_password == old_password:
            return Response(
                data='Пароли не должны совпадать',
                status=status.HTTP_400_BAD_REQUEST,
            )
        user.set_password(new_password)
        user.save()
        return Response(
            data='Пароль успешно изменен', status=status.HTTP_204_NO_CONTENT
        )

    @action(['GET'], detail=False)
    def subscriptions(self, request):
        user = request.user
        followers = User.objects.filter(following__user=user)
        page = self.paginate_queryset(followers)
        serializer = self.get_serializer(
            instance=page, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
