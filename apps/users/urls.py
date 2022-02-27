from django.urls import path

from .views import UserRegisterCheckView, UserRegisterView

urlpatterns = [
    path("check", UserRegisterCheckView.as_view(), name="user-check"),
    path("register", UserRegisterView.as_view(), name="register"),
]
