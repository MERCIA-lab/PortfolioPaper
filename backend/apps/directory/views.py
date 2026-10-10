from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.portfolio.models import Portfolio
from apps.portfolio.serializers import PortfolioPublicSerializer, PortfolioSerializer


class DirectoryView(APIView):
    def get(self, request):
        portfolios = Portfolio.objects.filter(is_public=True).order_by('-created_at')
        return Response(PortfolioPublicSerializer(portfolios, many=True).data)


class PortfolioPublicView(APIView):
    def get(self, request, slug):
        portfolio = get_object_or_404(Portfolio.objects.filter(is_public=True), slug=slug)
        return Response(PortfolioSerializer(portfolio).data)
