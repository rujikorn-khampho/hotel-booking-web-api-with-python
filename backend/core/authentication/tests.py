from django.contrib.auth.hashers import check_password
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.authentication.factories import UserFactory
from core.authentication.utils import User


class RegisterTests(APITestCase):
    def setUp(self) -> None:
        self.url = reverse('user-register')
        self.user = UserFactory.build()
        self.data = {
            'email': self.user.email,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'phone': self.user.phone,
            'address': self.user.address,
            'password': self.user.password,
            'confirm_password': self.user.password,
        }

    def test_register_user(self):
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=response.data)
        self.assertEqual(User.objects.count(), 1)

        user = User.objects.first()
        self.assertEqual(user.email, self.data.get('email'))
        self.assertEqual(user.first_name, self.data.get('first_name'))
        self.assertEqual(user.last_name, self.data.get('last_name'))
        self.assertEqual(user.phone, self.data.get('phone'))
        self.assertEqual(user.address, self.data.get('address'))
        self.assertTrue(check_password(self.data.get('password'), user.password))

    def test_register_user_password_mismatch(self):
        self.data['confirm_password'] = 'different_password'
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg=response.data)
        self.assertEqual(User.objects.count(), 0)

    def test_register_user_invalid_email(self):
        self.data['email'] = 'invalid_email'
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg=response.data)
        self.assertEqual(User.objects.count(), 0)


class ProfileTests(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.client.force_login(user=self.user)
        self.url = reverse('user-retrieve-profile')

    def test_retrieve_profile(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)

        self.assertEqual(response.data.get('email'), self.user.email)
        self.assertEqual(response.data.get('first_name'), self.user.first_name)
        self.assertEqual(response.data.get('last_name'), self.user.last_name)
        self.assertEqual(response.data.get('phone'), self.user.phone)
        self.assertEqual(response.data.get('address'), self.user.address)

    def test_retrieve_profile_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg=response.data)

    def test_update_profile(self):
        data = {
            'email': 'johndoe@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'phone': '1234567890',
            'address': '123 Main St',
        }
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)

        user = User.objects.first()
        self.assertEqual(user.email, data.get('email'))
        self.assertEqual(user.first_name, data.get('first_name'))
        self.assertEqual(user.last_name, data.get('last_name'))
        self.assertEqual(user.phone, data.get('phone'))
        self.assertEqual(user.address, data.get('address'))


class ChangePasswordTests(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.url = reverse('user-change-password')
        self.data = {
            'old_password': '+KGtjFuS+kww&7c)',
            'new_password': 'new_password',
            'confirm_new_password': 'new_password',
        }

    def test_change_password(self):
        response = self.client.put(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)

        user = User.objects.first()
        self.assertTrue(check_password(self.data.get('new_password'), user.password))

    def test_change_password_invalid(self):
        self.data['old_password'] = 'invalid_password'
        response = self.client.put(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg=response.data)

    def test_password_mismatch(self):
        self.data['confirm_new_password'] = 'different_password'
        response = self.client.put(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg=response.data)
