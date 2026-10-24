from django.urls import path

from .views import CsrfTokenView, LoginView, LogoutView, RegisterView, UserView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('csrf/', CsrfTokenView.as_view(), name='csrf'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/', UserView.as_view(), name='user'),
    path('refresh/', TokenRefreshView.as_view(), name="auth-refresh")

]
