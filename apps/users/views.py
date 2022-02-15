from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import (
    TokenBlacklistSerializer,
    TokenObtainPairSerializer,
)
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenObtainPairView,
    TokenRefreshView,
)

from apps.cores.permissions import IsOwner

from .models import User, UserDailyInfo, UserOption
from .serializers import (
    UserDetailSerializer,
    UserOptionSerializer,
    UserRegisterSerializer,
)


class UserRegisterView(generics.CreateAPIView):
    """
    유저 생성

    유저 회원가입 API
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        user_id = request.data["user_id"]
        nickname = request.data["nickname"]
        password = request.data["password"]
        user_option = request.data["options"]
        user = User.objects.create_user(
            user_id=user_id, nickname=nickname, password=password
        )
        UserOption.objects.create(user_id=user, **user_option)
        return Response({"result": "가입 완료"}, status=status.HTTP_201_CREATED)


class UserLoginView(TokenObtainPairView):
    """
    유저 로그인

    유저 로그인 API(access, refresh 토큰 반환)
    """


class UserLogoutView(TokenBlacklistView):
    """
    유저 로그아웃

    유저 로그아웃 API
    - refresh 토큰을 받아 token을 디비에서 만료시킴으로써 로그아웃 처리
    """

    permission_classes = [permissions.IsAuthenticated]


class UserDetailView(generics.ListAPIView):
    """
    유저 상세정보 조회

    유저 상세정보 API
    - 유저와 관련된 모든 정보를 반환
    """

    serializer_class = UserDetailSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        queryset = User.objects.filter(id=self.request.user.id)
        queryset.prefetch_related("option", "daily_info")
        return queryset


class UserDetailUpdateView(generics.UpdateAPIView):
    """
    유저 상세정보 수정

    유저 상세정보 수정 API
    - 유저와 관련된 정보 수정
    """

    serializer_class = UserOptionSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        queryset = User.objects.filter(id=self.request.user.id)
        queryset.prefetch_related("option")
        return queryset
