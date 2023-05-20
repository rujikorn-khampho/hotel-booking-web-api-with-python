from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from core.authentication.serializers import UserSerializer, RegisterSerializer, ProfileSerializer
from core.authentication.utils import User, CreateOnlyModelViewSet, ListOnlyModelViewSet


class RegisterViewSet(CreateOnlyModelViewSet):
    queryset = User.objects.order_by('-pk')
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class ProfileViewSet(ListOnlyModelViewSet):
    queryset = User.objects.order_by('-pk')
    serializer_class = ProfileSerializer

    def list(self, request, *args, **kwargs):
        instance = get_object_or_404(User, pk=request.user.pk)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.order_by('-pk')
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
