from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import CustomUser
from .serializers import UserCreateSerializer, UserReadSerializer


class CustomUserViewSet(viewsets.ModelViewSet):
    """"""

    queryset = CustomUser.objects.all()

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return UserReadSerializer
        return UserCreateSerializer

    @action(
        methods=('get',),
        detail=False,
    )
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
