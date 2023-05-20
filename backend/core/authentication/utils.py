from django.contrib.auth import get_user_model
from rest_framework import mixins, viewsets

User = get_user_model()


class CreateOnlyModelViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    pass


class ListOnlyModelViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    pass
