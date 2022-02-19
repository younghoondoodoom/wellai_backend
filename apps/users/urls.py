from django.urls import path
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import UserCheckView, UserDetailView, UserOptionUpdateView, UserRegisterView

urlpatterns = [
    path("check/", UserCheckView.as_view(), name="user-check"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("logout/", TokenBlacklistView.as_view(), name="logout"),
    path("detail/", UserDetailView.as_view(), name="user-detail"),
    path("option/", UserOptionUpdateView.as_view(), name="user-option-update"),
]
