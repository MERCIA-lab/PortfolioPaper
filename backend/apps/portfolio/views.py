from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Portfolio
from .serializers import PortfolioSerializer, PortfolioWriteSerializer


class PortfolioOwnView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        portfolio, _ = Portfolio.objects.get_or_create(user=request.user)
        return Response(PortfolioSerializer(portfolio).data)

    def post(self, request):
        portfolio, created = Portfolio.objects.get_or_create(user=request.user)
        serializer = PortfolioWriteSerializer(instance=portfolio, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        portfolio = serializer.save()
        return Response(PortfolioSerializer(portfolio).data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
