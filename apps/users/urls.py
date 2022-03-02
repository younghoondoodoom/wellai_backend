from django.urls import path
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .views import (
    UserMonthlyRecordView,
    UserOptionUpdateView,
    UserRegisterCheckView,
    UserRegisterView,
    UserWeeklyRecordView,
)

urlpatterns = [
    path("login", TokenObtainPairView.as_view(), name="login"),
    path("logout", TokenBlacklistView.as_view(), name="logout"),
    path("token/refresh", TokenRefreshView.as_view(), name="token-refresh"),
    path("token/verify", TokenVerifyView.as_view(), name="token-verify"),
    path("check", UserRegisterCheckView.as_view(), name="user-check"),
    path("option", UserOptionUpdateView.as_view(), name="user-option-update"),
    path("records/month/", UserMonthlyRecordView.as_view(), name="monthly-records"),
    path("records/week", UserWeeklyRecordView.as_view(), name="weekly-records"),
    path("register", UserRegisterView.as_view(), name="register"),
]
