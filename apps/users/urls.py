from django.urls import path

from .views import UserRegisterView

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    # path("login/", UserLoginView.as_view(), name="login"),
    # path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    #     path("login/"),
    #     path("logout/"),
]
