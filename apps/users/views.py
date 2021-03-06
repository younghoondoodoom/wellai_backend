from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Prefetch
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.cores.permissions import IsOwner
from apps.users.exceptions import EmailExistException, PasswordCheckException

from .models import User, UserDailyRecord, UserOption
from .serializers import (
    CustomTokenObtainPairSerializer,
    DateCheckSerializer,
    UserAnnualRecordSerializer,
    UserDailyRecordSerializer,
    UserMonthlyRecordSerializer,
    UserOptionSerializer,
    UserRegisterCheckSerializer,
    UserRegisterSerializer,
)
from .utils import get_decoded_token


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserRegisterCheckView(generics.CreateAPIView):
    serializer_class = UserRegisterCheckSerializer

    def post(self, request, *args, **kwargs):
        if request.data["password"] != request.data["confirm_password"]:
            raise PasswordCheckException()

        serializer = UserRegisterCheckSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            User.objects.get(email=request.data["email"])
            raise EmailExistException()
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_200_OK)


class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer


class UserOptionUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsOwner]
    serializer_class = UserOptionSerializer
    queryset = UserOption.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = User.objects.get(id=request.user.id)
        serializer = UserRegisterSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = True
        instance = UserOption.objects.get_or_create(user_id=request.user)[0]
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserAnnualRecordView(generics.ListAPIView):
    serializer_class = UserAnnualRecordSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        queryset = User.objects.filter(id=self.request.user.id).prefetch_related(
            Prefetch(
                "daily_record",
                queryset=UserDailyRecord.objects.filter(
                    exercise_date__year=timezone.now().year,
                ).order_by("exercise_date__month"),
            )
        )
        return queryset


class UserMonthlyRecordView(generics.ListAPIView):
    serializer_class = UserMonthlyRecordSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        date_serializer = DateCheckSerializer(data=self.request.query_params)
        date_serializer.is_valid(raise_exception=True)
        queryset = User.objects.filter(id=self.request.user.id).prefetch_related(
            Prefetch(
                "daily_record",
                queryset=UserDailyRecord.objects.filter(
                    exercise_date__month=self.request.query_params["month"],
                ).order_by("exercise_date"),
            )
        )
        return queryset


class UserRecordUpdateView(generics.CreateAPIView):
    serializer_class = UserDailyRecordSerializer
    permission_classes = [IsOwner]
