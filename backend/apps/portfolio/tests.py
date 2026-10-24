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

    def test_post_saves_all_profile_and_project_fields(self):
        response = self.client.post(
            reverse("portfolio-own"),
            {
                "full_name": "Portfolio Owner",
                "github": "https://github.com/portfolio-owner",
                "github_summary": "Open-source contributions.",
                "is_public": True,
                "projects": [
                    {
                        "title": "Portfolio Paper",
                        "category": "Web",
                        "technologies": "Django, JavaScript",
                        "description": "A portfolio application.",
                        "link": "https://example.com/project",
                    }
                ],
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        portfolio = Portfolio.objects.get(user=self.user)
        self.assertEqual(portfolio.github, "https://github.com/portfolio-owner")
        self.assertEqual(portfolio.github_summary, "Open-source contributions.")
        project = portfolio.projects.get()
        self.assertEqual(project.category, "Web")
        self.assertEqual(project.technologies, "Django, JavaScript")
