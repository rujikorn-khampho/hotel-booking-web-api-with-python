from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

from core.authentication.serializers import UserSerializer, RegisterSerializer, ProfileSerializer, \
    ChangePasswordSerializer
from core.authentication.utils import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.order_by('-pk')
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def get_object(self):
        return (
            self.request.user
            if self.action in ['profile', 'update_profile', 'change_password']
            else super().get_object()
        )

    @action(
        methods=['post'],
        detail=False,
        serializer_class=RegisterSerializer,
        permission_classes=[AllowAny],
    )
    def register(self, request):
        return super().create(request)

    @action(
        detail=False,
        serializer_class=ProfileSerializer,
        permission_classes=[IsAuthenticated],
    )
    def profile(self, request):
        return super().retrieve(request)

    @profile.mapping.put
    def update_profile(self, request):
        return super().update(request)

    @action(
        methods=['put'],
        detail=False,
        url_path='change-password',
        serializer_class=ChangePasswordSerializer,
        permission_classes=[IsAuthenticated],
    )
    def change_password(self, request):
        return super().update(request)
