from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.portfolio.models import Portfolio
from apps.portfolio.serializers import PortfolioDirectorySerializer, PortfolioPublicSerializer


class DirectoryView(APIView):
    def get(self, request):
        portfolios = Portfolio.objects.filter(is_public=True).prefetch_related('skills').order_by('-created_at')
        return Response(PortfolioDirectorySerializer(portfolios, many=True).data)


class PortfolioPublicView(APIView):
    def get(self, request, slug):
        portfolio = get_object_or_404(
            Portfolio.objects.filter(is_public=True).prefetch_related(
                'education',
                'experience',
                'skills',
                'projects',
            ),
            slug=slug,
        )
        return Response(PortfolioPublicSerializer(portfolio).data)
