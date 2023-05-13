from rest_framework import viewsets

from core.authentication.serializers import UserSerializer
from core.authentication.utils import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.order_by('-pk')
    serializer_class = UserSerializer
