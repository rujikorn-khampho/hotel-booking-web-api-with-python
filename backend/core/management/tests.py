from typing import Optional, TypedDict

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.authentication.factories import UserFactory
from core.management.factories import RoomTypeFactory, EquipmentFactory
from core.management.models import RoomType, Equipment


class RoomTypeData(TypedDict):
    name: str
    description: str


class RoomTypeTests(APITestCase):
    def setUp(self) -> None:
        self.admin_user = UserFactory(is_staff=True, is_superuser=True)
        self.client.force_login(user=self.admin_user)
        self.model = RoomType

    def get_request_url(self, pk: Optional[int] = None) -> str:
        url_name = self.model.__name__.lower()

        return (
            reverse(f'{url_name}-detail', args=[pk])
            if pk else reverse(f'{url_name}-list')
        )

    @staticmethod
    def get_request_body() -> RoomTypeData:
        room_type = RoomTypeFactory.build()

        return {
            'name': room_type.name,
            'description': room_type.description,
        }

    @staticmethod
    def create_room_type() -> RoomType:
        return RoomTypeFactory()

    def test_create_room_type(self):
        url = self.get_request_url()
        data = self.get_request_body()
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=response.data)
        self.assertEqual(self.model.objects.count(), 1)

        room_type = self.model.objects.first()
        self.assertEqual(room_type.name, data.get('name'))
        self.assertEqual(room_type.description, data.get('description'))

    def test_list_room_type(self):
        room_type = self.create_room_type()
        url = self.get_request_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
        self.assertEqual(len(response.data), 1)

        names, descriptions = zip(
            *((data.get('name'), data.get('description')) for data in response.data)
        )
        self.assertIn(room_type.name, names)
        self.assertIn(room_type.description, descriptions)

    def test_retrieve_room_type(self):
        room_type = self.create_room_type()
        url = self.get_request_url(room_type.pk)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
        self.assertEqual(response.data.get('name'), room_type.name)
        self.assertEqual(response.data.get('description'), room_type.description)

    def test_update_room_type(self):
        room_type = self.create_room_type()
        url = self.get_request_url(room_type.pk)

        data = self.get_request_body()
        data['name'] = 'Name updated'
        data['description'] = 'Description updated'

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)

        room_type.refresh_from_db()
        self.assertEqual(room_type.name, data.get('name'))
        self.assertEqual(room_type.description, data.get('description'))

    def test_delete_room_type(self):
        room_type = self.create_room_type()
        url = self.get_request_url(room_type.pk)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, msg=response.data)
        self.assertEqual(self.model.objects.count(), 0)


class EquipmentData(TypedDict):
    name: str
    description: str


class EquipmentTests(APITestCase):
    def setUp(self) -> None:
        self.admin_user = UserFactory(is_staff=True, is_superuser=True)
        self.client.force_login(user=self.admin_user)
        self.model = Equipment

    def get_request_url(self, pk: Optional[int] = None) -> str:
        url_name = self.model.__name__.lower()

        return (
            reverse(f'{url_name}-detail', args=[pk])
            if pk else reverse(f'{url_name}-list')
        )

    @staticmethod
    def get_request_body() -> EquipmentData:
        equipment = EquipmentFactory.build()

        return {
            'name': equipment.name,
            'description': equipment.description,
        }

    @staticmethod
    def create_equipment() -> Equipment:
        return EquipmentFactory()

    def test_create_equipment(self):
        url = self.get_request_url()
        data = self.get_request_body()
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=response.data)
        self.assertEqual(self.model.objects.count(), 1)

        equipment = self.model.objects.first()
        self.assertEqual(equipment.name, data.get('name'))
        self.assertEqual(equipment.description, data.get('description'))

    def test_list_equipment(self):
        equipment = self.create_equipment()
        url = self.get_request_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
        self.assertEqual(len(response.data), 1)

        names, descriptions = zip(
            *((data.get('name'), data.get('description')) for data in response.data)
        )
        self.assertIn(equipment.name, names)
        self.assertIn(equipment.description, descriptions)

    def test_retrieve_equipment(self):
        equipment = self.create_equipment()
        url = self.get_request_url(equipment.pk)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
        self.assertEqual(response.data.get('name'), equipment.name)
        self.assertEqual(response.data.get('description'), equipment.description)

    def test_update_equipment(self):
        equipment = self.create_equipment()
        url = self.get_request_url(equipment.pk)

        data = self.get_request_body()
        data['name'] = 'Name updated'
        data['description'] = 'Description updated'

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)

        equipment.refresh_from_db()
        self.assertEqual(equipment.name, data.get('name'))
        self.assertEqual(equipment.description, data.get('description'))

    def test_delete_equipment(self):
        equipment = self.create_equipment()
        url = self.get_request_url(equipment.pk)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, msg=response.data)
        self.assertEqual(self.model.objects.count(), 0)
