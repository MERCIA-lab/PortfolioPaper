from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


class AccountApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="existing@example.com",
            username="existing-user",
            password="correct-horse-battery",
        )

    def test_invalid_login_returns_unauthorized(self):
        response = self.client.post(
            reverse("login"),
            {"email": self.user.email, "password": "incorrect-password"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_registration_rejects_duplicate_username(self):
        response = self.client.post(
            reverse("register"),
            {
                "email": "new@example.com",
                "username": self.user.username,
                "password": "correct-horse-battery",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.json())

    def test_csrf_endpoint_sets_cookie_for_frontend_requests(self):
        response = self.client.get(reverse("csrf"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("csrfToken", response.json())
        self.assertIn("csrftoken", response.cookies)

    def test_logout_uses_refresh_cookie_and_clears_cookies_without_valid_access_token(self):
        refresh = RefreshToken.for_user(self.user)
        self.client.cookies["access_token"] = "expired-access-token"
        self.client.cookies["refresh_token"] = str(refresh)

        response = self.client.post(reverse("logout"), {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)
        self.assertEqual(response.cookies["access_token"]["max-age"], 0)
        self.assertEqual(response.cookies["refresh_token"]["max-age"], 0)
