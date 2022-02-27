from django.urls import path

from .views import UserRegisterCheckView

urlpatterns = [
    path("check", UserRegisterCheckView.as_view(), name="user-check"),
]
