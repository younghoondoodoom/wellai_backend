import json

import requests
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, mixins, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

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


class KakaoLoginView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        kakao_token = request.data["token"]
        url = "https://kapi.kakao.com/v2/user/me"
        headers = {
            "Authorization": f"Bearer {kakao_token}",
            "Content-type": "application/x-www-form-urlencoded; charset=utf-8",
        }
        response = requests.post(url, headers=headers)
        response = json.loads(response.text)
        # TODO: social 나머지 부분 구현 필요
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserOptionUpdateView(APIView):
    permission_classes = [IsOwner]

    def get(self, request, format=None):
        user = User.objects.get(id=request.user.id)
        serializer = UserRegisterSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = UserOptionSerializer(data=request.data)
        if serializer.is_valid():
            user = UserOption.objects.get_or_create(user_id=request.user)[0]
            user.gender = request.data["gender"]
            user.height = request.data["height"]
            user.weight = request.data["weight"]
            user.is_stand = request.data["stand"]
            user.is_sit = request.data["sit"]
            user.is_balance = request.data["balance"]
            user.is_core = request.data["core"]
            user.is_leg = request.data["leg"]
            user.is_back = request.data["back"]
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


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
