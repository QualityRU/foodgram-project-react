from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Subscribe, User
from .serializers import (
    SubscribeSerializer,
    SubscriptionSerializer,
    UserCreateSerializer,
    UserListSerializer,
    UserSetPasswordSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    """Представление пользователя."""

    queryset = User.objects.all()
    http_method_names = [
        'get',
        'post',
        'delete',
    ]
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
        if self.action in ('list', 'retrieve', 'me'):
            return UserListSerializer
        if self.action == 'set_password':
            return UserSetPasswordSerializer
        if self.action == 'subscriptions':
            return SubscriptionSerializer
        if self.action == 'subscribe':
            return SubscribeSerializer

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
        """Получение списка подписок пользователя."""

        user = request.user
        subscribers = User.objects.filter(subscriber__user=user)
        page = self.paginate_queryset(subscribers)
        serializer = self.get_serializer(
            instance=page, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(['POST', 'DELETE'], detail=True)
    def subscribe(self, request, pk=None):
        """Добавление и удаление подписок пользователя."""

        if self.request.method == 'POST':
            return self.subscribe_post(request, pk)
        if self.request.method == 'DELETE':
            return self.subscribe_delete(pk)

    def subscribe_post(self, request, pk):
        serializer = self.get_serializer(
            data=request.data, context={'request': request, 'id': pk}
        )
        serializer.is_valid(raise_exception=True)
        response_data = serializer.save(id=pk)
        return Response(data=response_data, status=status.HTTP_201_CREATED)

    def subscribe_delete(self, pk):
        user = self.request.user
        author = get_object_or_404(User, pk=pk)
        subscribe = get_object_or_404(Subscribe, user=user, author=author)
        subscribe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
