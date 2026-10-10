from django.urls import path

from .views import PortfolioOwnView

urlpatterns = [
    path('', PortfolioOwnView.as_view(), name='portfolio-own'),
]
