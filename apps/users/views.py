from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Prefetch, Q
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.response import Response

from apps.cores.permissions import IsOwner
from apps.users.exceptions import EmailExistException, PasswordCheckException

from .models import User, UserDailyRecord, UserOption
from .serializers import (
    DateCheckSerializer,
    UserDailyRecordSerializer,
    UserMonthlyRecordSerializer,
    UserOptionSerializer,
    UserRegisterCheckSerializer,
    UserRegisterSerializer,
    UserWeeklyRecordSerializer,
)


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
                    exercise_date__year=self.request.query_params["year"],
                    exercise_date__month=self.request.query_params["month"],
                ),
            )
        )
        return queryset


class UserWeeklyRecordView(generics.ListAPIView):
    serializer_class = UserWeeklyRecordSerializer
    permission_classes = [IsOwner]
    week = timezone.now().isocalendar()[1]

    def get_queryset(self):
        queryset = User.objects.filter(id=self.request.user.id).prefetch_related(
            Prefetch(
                "daily_record",
                queryset=UserDailyRecord.objects.filter(
                    exercise_week=self.week,
                ).order_by("exercise_date"),
            )
        )
        return queryset


class UserRecordUpdateView(generics.CreateAPIView):
    serializer_class = UserDailyRecordSerializer
    permission_classes = [IsOwner]
