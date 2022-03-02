from django.db.models import Prefetch, Q
from django.utils import timezone
from rest_framework import generics, mixins, permissions, status

from apps.cores.permissions import IsOwner

from .models import User, UserDailyRecord
from .serializers import (
    DateCheckSerializer,
    UserMonthlyRecordSerializer,
    UserWeeklyRecordSerializer,
)


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
                ),
            )
        )
        return queryset
