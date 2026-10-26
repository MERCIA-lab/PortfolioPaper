import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from apps.accounts.models import User
from .models import Experience, Portfolio, Skill


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

    def test_post_saves_nested_multipart_data_from_frontend(self):
        response = self.client.post(
            reverse("portfolio-own"),
            {
                "full_name": "Portfolio Owner",
                "experience": json.dumps([
                    {
                        "company": "Example Co",
                        "role": "Developer",
                        "location": "London",
                        "start_date": "2022",
                        "end_date": "Present",
                        "description": "Built useful software.",
                    }
                ]),
                "education": "[]",
                "skills": json.dumps([{"name": "Python", "level": "4"}]),
                "projects": "[]",
            },
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["experience"][0]["location"], "London")
        experience = Experience.objects.get(portfolio__user=self.user)
        self.assertEqual(experience.location, "London")
        skill = Skill.objects.get(portfolio__user=self.user)
        self.assertEqual(skill.name, "Python")

    def test_post_rejects_invalid_nested_multipart_json(self):
        response = self.client.post(
            reverse("portfolio-own"),
            {"experience": "[invalid"},
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("experience", response.data)
