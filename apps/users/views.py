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

from .models import User, UserInfo, UserOption
from .serializers import (
    UserDetailSerializer,
    UserInfoSerializer,
    UserRegisterSerializer,
)


class UserRegisterView(generics.CreateAPIView):
    """
    유저 생성

    유저 회원가입 API
    """

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

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenObtainPairSerializer,
            status.HTTP_401_UNAUTHORIZED: "만료되거나 유효하지 않은 토큰",
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UserLogoutView(TokenBlacklistView):
    """
    유저 로그아웃

    유저 로그아웃 API
    - refresh 토큰을 받아 token을 디비에서 만료시킴으로써 로그아웃 처리
    """

    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenBlacklistSerializer,
            status.HTTP_401_UNAUTHORIZED: "만료되거나 유효하지 않은 토큰",
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(self, request, *args, **kwargs)


class UserDetailView(generics.ListAPIView):
    """
    유저 상세정보

    유저 상세정보 API
    - 유저와 관련된 모든 정보를 반환
    """

    serializer_class = UserDetailSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        queryset = User.objects.filter(id=self.request.user.id)
        queryset.prefetch_related("option", "info")
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        print(queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: UserDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: "권한 없음",
        }
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
