from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, mixins, permissions, status
from rest_framework.response import Response

from apps.cores.permissions import IsOwner

from .models import User, UserDailyInfo, UserOption
from .serializers import (
    UserDetailSerializer,
    UserOptionSerializer,
    UserRegisterSerializer,
    UserSerializer,
)


class UserCheckView(generics.CreateAPIView):
    """
    유저 가입 정보 체크

    유저 기본정보 회원가입시 체크하는 API
    """

    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"message": "기본 정보 통과"}, status=status.HTTP_200_OK)
        else:
            error_list = serializer.errors
            return Response(error_list, status=status.HTTP_400_BAD_REQUEST)


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
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                user_id=user_id, nickname=nickname, password=password
            )
            UserOption.objects.create(user_id=user, **user_option)
            return Response({"message": "가입 완료"}, status=status.HTTP_201_CREATED)
        else:
            error_list = serializer.errors
            return Response(error_list, status=status.HTTP_400_BAD_REQUEST)


class UserOptionUpdateView(generics.UpdateAPIView):
    """
    유저 정보 수정

    유저 정보 수정 API
    - 유저와 관련된 추가 정보 수정
    """

    serializer_class = UserOptionSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        queryset = User.objects.get(id=self.request.user.id)
        queryset.prefetch_related("option")
        return queryset

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = UserOption.user_id.get(user_id=self.request.user)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


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
