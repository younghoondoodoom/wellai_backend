from django.urls import path
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .views import (
    CustomTokenObtainPairView,
    UserAnnualRecordView,
    UserMonthlyRecordView,
    UserOptionUpdateView,
    UserRecordUpdateView,
    UserRegisterCheckView,
    UserRegisterView,
)

urlpatterns = [
    path("login", CustomTokenObtainPairView.as_view(), name="login"),
    path("logout", TokenBlacklistView.as_view(), name="logout"),
    path("token/refresh", TokenRefreshView.as_view(), name="token-refresh"),
    path("token/verify", TokenVerifyView.as_view(), name="token-verify"),
    path("check", UserRegisterCheckView.as_view(), name="user-check"),
    path("option", UserOptionUpdateView.as_view(), name="user-option-update"),
    path("records/year", UserAnnualRecordView.as_view(), name="annual-records"),
    path("records/", UserMonthlyRecordView.as_view(), name="monthly-records"),
    path("records", UserRecordUpdateView.as_view(), name="records-update"),
    path("register", UserRegisterView.as_view(), name="register"),
]
