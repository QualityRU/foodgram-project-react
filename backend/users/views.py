from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import User
from .serializers import (
    UserCreateSerializer,
    UserReadSerializer,
    UserSetPasswordSerializer,
)

DEFAULT_PERMISSION_CLASSES = (permissions.IsAuthenticated,)


class UserViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """Представление пользователя."""

    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)

    def get_serializer_class(self):
        """Определение действия с сериализатором."""
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action == 'set_password':
            return UserSetPasswordSerializer
        elif self.action in ('list', 'retrieve', 'me'):
            return UserReadSerializer

    @action(
        methods=('GET',),
        permission_classes=DEFAULT_PERMISSION_CLASSES,
        detail=False,
    )
    def me(self, request):
        """Текущий пользователь."""
        serializer = self.get_serializer(request.user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=('POST',),
        serializer_class=UserSetPasswordSerializer,
        permission_classes=DEFAULT_PERMISSION_CLASSES,
        detail=False,
    )
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
