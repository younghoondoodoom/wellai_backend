from django.urls import path
from rest_framework_simplejwt.views import TokenBlacklistView, TokenObtainPairView

urlpatterns = [
    path("login", TokenObtainPairView.as_view(), name="login"),
    path("logout", TokenBlacklistView.as_view(), name="logout"),
]
