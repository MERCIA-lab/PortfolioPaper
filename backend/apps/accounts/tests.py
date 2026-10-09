from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import User


class UserAuthAPITests(APITestCase):
    def test_register_and_login_flow(self):
        payload = {
            'email': 'test@example.com',
            'username': 'tester',
            'password': 'securepass123',
        }

        register_response = self.client.post(reverse('register'), payload, format='json')
        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='test@example.com').exists())

        login_response = self.client.post(reverse('login'), payload, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn('email', login_response.data)

    def test_user_profile_requires_login(self):
        response = self.client.get(reverse('user'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
