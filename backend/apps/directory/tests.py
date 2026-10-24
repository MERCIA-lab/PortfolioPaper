from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from apps.accounts.models import User
from apps.portfolio.models import Education, Experience, Portfolio, Project, Skill


class PublicDirectoryApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="portfolio@example.com",
            username="portfolio-user",
            password="correct-horse-battery",
        )
        self.portfolio = Portfolio.objects.create(
            user=self.user,
            full_name="Portfolio User",
            job_title="Software Engineer",
            summary="A portfolio summary.",
            phone="555-0100",
            email=self.user.email,
            location="London",
            github="https://github.com/portfolio-user",
            github_summary="Open-source contributions.",
            is_public=True,
        )
        Experience.objects.create(
            portfolio=self.portfolio,
            company="Example Co",
            role="Developer",
            start_date="2022",
            end_date="Present",
            description="Built useful software.",
        )
        Education.objects.create(
            portfolio=self.portfolio,
            school="Example University",
            degree="Computer Science",
            start_year="2018",
            end_year="2022",
        )
        Skill.objects.create(portfolio=self.portfolio, name="Python", level=4)
        Project.objects.create(
            portfolio=self.portfolio,
            title="Portfolio Paper",
            category="Web",
            technologies="Django, JavaScript",
            description="A portfolio application.",
            link="https://example.com/project",
        )

    def test_directory_lists_public_profiles_with_searchable_skills(self):
        response = self.client.get(reverse("directory"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["slug"], self.portfolio.slug)
        self.assertEqual(response.data[0]["skills"][0]["name"], "Python")
        self.assertNotIn("email", response.data[0])

    def test_public_profile_detail_returns_the_complete_cv(self):
        response = self.client.get(
            reverse("portfolio-public-detail", kwargs={"slug": self.portfolio.slug})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user.email)
        self.assertEqual(response.data["github_summary"], "Open-source contributions.")
        self.assertEqual(response.data["experience"][0]["company"], "Example Co")
        self.assertEqual(response.data["education"][0]["school"], "Example University")
        self.assertEqual(response.data["skills"][0]["name"], "Python")
        self.assertEqual(response.data["projects"][0]["technologies"], "Django, JavaScript")

    def test_private_profile_is_excluded_and_not_available_by_slug(self):
        self.portfolio.is_public = False
        self.portfolio.save()

        directory_response = self.client.get(reverse("directory"))
        detail_response = self.client.get(
            reverse("portfolio-public-detail", kwargs={"slug": self.portfolio.slug})
        )

        self.assertEqual(directory_response.status_code, status.HTTP_200_OK)
        self.assertEqual(directory_response.data, [])
        self.assertEqual(detail_response.status_code, status.HTTP_404_NOT_FOUND)
