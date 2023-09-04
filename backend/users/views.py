from django.conf import settings
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import CustomUser
from .serializers import CustomUserCreateSerializer, CustomUserReadSerializer


class CustomUserViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """"""

    queryset = CustomUser.objects.all()
    permission_classes = (permissions.AllowAny,)
    default_permission_classes = settings.REST_FRAMEWORK.get(
        'DEFAULT_PERMISSION_CLASSES'
    )

    def get_serializer_class(self):
        if self.action == 'create':
            return CustomUserCreateSerializer
        if self.action in ('list', 'retrieve', 'me'):
            return CustomUserReadSerializer

    @action(
        methods=('get',),
        permission_classes=default_permission_classes,
        detail=False,
    )
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
