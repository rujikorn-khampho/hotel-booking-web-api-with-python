from rest_framework import status

from core.common.utils.api_test_case import CustomAPITestCase
from core.common.utils.nested_dict import get_value_from_nested_dict
from core.management.factories import AmenityFactory
from core.management.models import Hotel


class HotelTests(CustomAPITestCase):
    model = Hotel
    factory = AmenityFactory

    def get_request_body(self):
        instance = self.factory()
        return {
            'rooms': [
                {
                    'amenities': [
                        {
                            'quantity': instance.quantity,
                            'equipment': instance.equipment.pk,
                        }
                    ],
                    'name': instance.room.name,
                    'price': instance.room.price,
                    'is_available': instance.room.is_available,
                    'type': instance.room.type.pk,
                }
            ],
            'name': instance.room.hotel.name,
            'description': instance.room.hotel.description,
            'address': instance.room.hotel.address,
        }

    def test_create_action(self):
        url = self.get_request_url()
        data = self.get_request_body()
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=response.data)
        self.assertEqual(self.model.objects.count(), 2)

        instance = self.model.objects.first()
        self.assertEqual(instance.name, data.get('name'))
        self.assertEqual(instance.description, data.get('description'))
        self.assertEqual(instance.address, data.get('address'))

    def test_list_action(self):
        instance = self.create_instance()
        url = self.get_request_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
        self.assertEqual(len(response.data), 1)

        names, descriptions, addresses = zip(
            *(
                (data.get('name'), data.get('description'), data.get('address'))
                for data in response.data
            )
        )
        self.assertIn(instance.room.hotel.name, names)
        self.assertIn(instance.room.hotel.description, descriptions)
        self.assertIn(instance.room.hotel.address, addresses)

    def test_retrieve_action(self):
        instance = self.create_instance()
        url = self.get_request_url(instance.room.hotel.pk)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)

        for room in response.data.get('rooms'):
            for amenity in room.get('amenities'):
                self.assertEqual(
                    get_value_from_nested_dict(amenity, 'equipment.name'),
                    instance.equipment.name,
                )
                self.assertEqual(
                    get_value_from_nested_dict(amenity, 'equipment.description'),
                    instance.equipment.description,
                )

            self.assertEqual(
                get_value_from_nested_dict(room, 'type.name'),
                instance.room.type.name,
            )
            self.assertEqual(
                get_value_from_nested_dict(room, 'type.description'),
                instance.room.type.description,
            )
            self.assertEqual(room.get('name'), instance.room.name)
            self.assertEqual(room.get('price'), str(instance.room.price))
            self.assertEqual(room.get('is_available'), instance.room.is_available)

        self.assertEqual(response.data.get('name'), instance.room.hotel.name)
        self.assertEqual(response.data.get('description'), instance.room.hotel.description)
        self.assertEqual(response.data.get('address'), instance.room.hotel.address)

    def test_update_action(self):
        instance = self.create_instance()
        url = self.get_request_url(instance.room.hotel.pk)

        data = self.get_request_body()
        data['name'] = 'Name updated'
        data['description'] = 'Description updated'
        data['address'] = 'Address updated'

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)

        instance.room.hotel.refresh_from_db()
        self.assertEqual(instance.room.hotel.name, data.get('name'))
        self.assertEqual(instance.room.hotel.description, data.get('description'))
        self.assertEqual(instance.room.hotel.address, data.get('address'))

    def test_destroy_action(self):
        instance = self.create_instance()
        url = self.get_request_url(instance.room.hotel.pk)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, msg=response.data)
        self.assertEqual(self.model.objects.count(), 0)
