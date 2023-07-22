from typing import Dict, Any

from rest_framework import status

from core.common.utils.api_test_case import CustomAPITestCase
from core.management.factories import RoomTypeFactory
from core.management.models import RoomType


class RoomTypeTests(CustomAPITestCase):
    model = RoomType
    factory = RoomTypeFactory

    def get_request_body(self) -> Dict[str, Any]:
        instance = self.factory.build()
        return {
            'name': instance.name,
            'description': instance.description,
        }

    def test_create_action(self):
        url = self.get_request_url()
        data = self.get_request_body()
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=response.data)
        self.assertEqual(self.model.objects.count(), 1)

        instance = self.model.objects.first()
        self.assertEqual(instance.name, data.get('name'))
        self.assertEqual(instance.description, data.get('description'))

    def test_list_action(self):
        instance = self.create_instance()
        url = self.get_request_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
        self.assertEqual(len(response.data), 1)

        names, descriptions = zip(
            *((data.get('name'), data.get('description')) for data in response.data)
        )
        self.assertIn(instance.name, names)
        self.assertIn(instance.description, descriptions)

    def test_retrieve_action(self):
        instance = self.create_instance()
        url = self.get_request_url(instance.pk)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
        self.assertEqual(response.data.get('name'), instance.name)
        self.assertEqual(response.data.get('description'), instance.description)

    def test_update_action(self):
        instance = self.create_instance()
        url = self.get_request_url(instance.pk)

        data = self.get_request_body()
        data['name'] = 'Name updated'
        data['description'] = 'Description updated'

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)

        instance.refresh_from_db()
        self.assertEqual(instance.name, data.get('name'))
        self.assertEqual(instance.description, data.get('description'))

    def test_destroy_action(self):
        instance = self.create_instance()
        url = self.get_request_url(instance.pk)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, msg=response.data)
        self.assertEqual(self.model.objects.count(), 0)
