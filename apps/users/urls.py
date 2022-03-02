from django.urls import path
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .views import UserMonthlyRecordView, UserWeeklyRecordView

urlpatterns = [
    path("login", TokenObtainPairView.as_view(), name="login"),
    path("logout", TokenBlacklistView.as_view(), name="logout"),
    path("token/refresh", TokenRefreshView.as_view(), name="token-refresh"),
    path("token/verify", TokenVerifyView.as_view(), name="token-verify"),
    path("records/month", UserMonthlyRecordView.as_view(), name="monthly-records"),
    path("records/week", UserWeeklyRecordView.as_view(), name="weekly-records"),
]
