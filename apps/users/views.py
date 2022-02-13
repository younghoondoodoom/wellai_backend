from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenBlacklistSerializer
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenObtainPairView,
    TokenRefreshView,
)

from .models import User, UserInfo, UserOption
from .serializers import (
    MyTokenObtainPairSerializer,
    UserDetailSerializer,
    UserRegisterSerializer,
)


class UserRegisterView(generics.CreateAPIView):
    """
    유저 생성

    유저 회원가입 API
    """

    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegisterSerializer

    @swagger_auto_schema(
        responses={
            status.HTTP_201_CREATED: "가입 완료",
            status.HTTP_401_UNAUTHORIZED: "인증 필요",
        }
    )
    def create(self, request, *args, **kwargs):
        user_id = request.data["user_id"]
        nickname = request.data["nickname"]
        password = request.data["password"]
        user_option = request.data["option"]
        user = User.objects.create_user(
            user_id=user_id, nickname=nickname, password=password
        )
        UserOption.objects.create(user_id=user, **user_option)
        return Response(status=status.HTTP_201_CREATED)


class UserLoginView(TokenObtainPairView):
    """
    유저 로그인

    유저 로그인 API(access, refresh 토큰 반환)
    """

    serializer_class = MyTokenObtainPairSerializer


class UserLogoutView(TokenBlacklistView):
    """
    유저 로그아웃

    유저 로그아웃 API
    - refresh 토큰을 받아 token을 디비에서 만료시킴으로써 로그아웃 처리
    """

    serializer_class = TokenBlacklistSerializer
