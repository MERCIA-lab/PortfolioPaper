from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from apps.accounts.models import User
from .models import Portfolio


class PortfolioApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="owner@example.com",
            username="portfolio-owner",
            password="correct-horse-battery",
        )
        self.client.force_authenticate(user=self.user)

    def test_get_creates_an_empty_portfolio(self):
        response = self.client.get(reverse("portfolio-own"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        portfolio = Portfolio.objects.get(user=self.user)
        self.assertEqual(portfolio.full_name, "")
        self.assertEqual(portfolio.slug, self.user.username)
