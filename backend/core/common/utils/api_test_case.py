from typing import Type, Optional

import factory
from django.db import models
from django.urls import reverse
from rest_framework.test import APITestCase

from core.authentication.factories import UserFactory


class CustomAPITestCase(APITestCase):
    model: Type[models.Model]
    factory: Type[factory.django.DjangoModelFactory]

    def setUp(self) -> None:
        self.admin_user = UserFactory(is_staff=True, is_superuser=True)
        self.client.force_login(user=self.admin_user)

    def get_request_url(self, pk: Optional[int] = None) -> str:
        url_name = self.model.__name__.lower()
        return (
            reverse(f'{url_name}-detail', args=[pk])
            if pk else reverse(f'{url_name}-list')
        )

    def create_instance(self):
        return self.factory()
