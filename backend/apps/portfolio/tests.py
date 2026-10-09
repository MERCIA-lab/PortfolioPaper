from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.models import User
from apps.portfolio.models import Portfolio


class PortfolioAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='portfolio@example.com',
            username='portfolio-user',
            password='strongpass123',
        )
        self.client.force_authenticate(user=self.user)

    def test_user_can_create_and_get_own_portfolio(self):
        payload = {
            'full_name': 'Jane Doe',
            'job_title': 'Software Engineer',
            'summary': 'Full-stack developer',
            'is_public': True,
            'education': [
                {'school': 'University of Technology', 'degree': 'BSc Computer Science', 'start_year': '2015', 'end_year': '2019'}
            ],
            'experience': [
                {'company': 'Acme', 'role': 'Developer', 'start_date': '2020', 'end_date': '2024', 'description': 'Built products'}
            ],
            'skills': [
                {'name': 'Python', 'level': 5},
            ],
            'projects': [
                {'title': 'Portfolio App', 'description': 'Personal site', 'link': 'https://example.com'}
            ],
        }

        create_response = self.client.post(reverse('portfolio-own'), payload, format='json')
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Portfolio.objects.filter(user=self.user).count(), 1)

        get_response = self.client.get(reverse('portfolio-own'))
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(get_response.data['full_name'], 'Jane Doe')
        self.assertEqual(len(get_response.data['education']), 1)

    def test_private_portfolio_is_not_in_directory(self):
        private = Portfolio.objects.create(
            user=self.user,
            full_name='Jane Doe',
            job_title='Developer',
            summary='Private summary',
            slug='jane-doe',
            is_public=False,
        )

        other_user = User.objects.create_user(
            email='other@example.com',
            username='other-user',
            password='strongpass123',
        )
        Portfolio.objects.create(
            user=other_user,
            full_name='John Smith',
            job_title='Designer',
            summary='Public summary',
            slug='john-smith',
            is_public=True,
        )

        response = self.client.get('/api/directory/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        slugs = [item['slug'] for item in response.data]
        self.assertNotIn(private.slug, slugs)
        self.assertIn('john-smith', slugs)
