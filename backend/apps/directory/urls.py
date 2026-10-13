from django.urls import path

from .views import DirectoryView, PortfolioPublicView

urlpatterns = [
    path('', DirectoryView.as_view(), name='directory'),
    path('<slug:slug>/', PortfolioPublicView.as_view(), name='portfolio-public-detail'),
]
