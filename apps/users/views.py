from django.db.models import Prefetch, Q
from django.utils import timezone
from rest_framework import generics, mixins, permissions, status

from apps.cores.permissions import IsOwner

from .models import User, UserDailyRecord
from .serializers import UserMonthlyRecordSerializer, UserWeeklySummarySerializer


class UserMonthlyRecordView(generics.ListAPIView):
    serializer_class = UserMonthlyRecordSerializer
    permission_classes = [IsOwner]
    current_month = timezone.now().strftime("%m")
    current_year = timezone.now().strftime("%Y")

    def get_queryset(self):
        queryset = User.objects.filter(id=self.request.user.id).prefetch_related(
            Prefetch(
                "daily_record",
                queryset=UserDailyRecord.objects.filter(
                    exercise_date__year=self.current_year,
                    exercise_date__month=self.current_month,
                ),
            )
        )
        return queryset


class UserWeeklyRecordView(generics.ListAPIView):
    serializer_class = UserWeeklySummarySerializer
    permission_classes = [IsOwner]
    week = timezone.now().isocalendar()[1]

    def get_queryset(self):
        print(self.week)
        queryset = User.objects.filter(id=self.request.user.id).prefetch_related(
            Prefetch(
                "daily_record",
                queryset=UserDailyRecord.objects.filter(
                    exercise_week=self.week,
                ),
            )
        )
        return queryset
