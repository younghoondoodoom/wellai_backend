from django.contrib.auth.models import update_last_login
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import EmailValidator
from django.db.models import F, Q, Sum
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings

from .models import User, UserDailyRecord, UserOption
from .utils import get_calories
from .validators import PasswordValidator


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        user = User.objects.get(email=attrs["email"])
        nickname = user.nickname
        data["nickname"] = nickname
        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


class UserRegisterCheckSerializer(serializers.Serializer):
    email = serializers.EmailField(validators=[EmailValidator()])
    password = serializers.CharField(
        max_length=128, min_length=8, validators=[PasswordValidator()]
    )
    confirm_password = serializers.CharField(
        max_length=128, min_length=8, validators=[PasswordValidator()]
    )


class UserOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserOption
        fields = (
            "modified_at",
            "created_at",
            "gender",
            "height",
            "weight",
            "is_stand",
            "is_sit",
            "is_balance",
            "is_core",
            "is_leg",
            "is_back",
        )
        excludes = (
            "id",
            "user_id",
        )
        read_only_fields = ("modified_at", "created_at")


class UserRegisterSerializer(serializers.ModelSerializer):
    options = UserOptionSerializer(source="option")
    password = serializers.CharField(
        max_length=128, validators=[PasswordValidator()], write_only=True
    )

    class Meta:
        model = User
        read_only_fields = ("nickname",)
        fields = ("email", "nickname", "password", "options")

    def create(self, validated_data):
        options_validated_data = validated_data.pop("option")
        user = User.objects.create_user(**validated_data)
        options_validated_data["user_id"] = user
        options_serializer = self.fields["options"]
        options_serializer.create(options_validated_data)
        return user


class UserDailyRecordSerializer(serializers.ModelSerializer):
    exercise_day = serializers.SerializerMethodField()
    year = serializers.SerializerMethodField()
    month = serializers.SerializerMethodField()
    day = serializers.SerializerMethodField()

    def get_exercise_day(self, obj):
        return obj.exercise_date.weekday()

    def get_year(self, obj):
        return obj.exercise_date.year

    def get_month(self, obj):
        return obj.exercise_date.month

    def get_day(self, obj):
        return obj.exercise_date.day

    class Meta:
        model = UserDailyRecord
        fields = (
            "exercise_date",
            "exercise_week",
            "exercise_day",
            "year",
            "month",
            "day",
            "exercise_duration",
            "calories_total",
        )
        read_only_fields = ("created_at", "calories_total")

    def create(self, validated_data):
        user = self.context["request"].user
        exercise_duration = round(int(validated_data["exercise_duration"]) / 60)
        exercise_date = validated_data["exercise_date"]
        user_option = UserOption.objects.get(user_id=user)
        calories = get_calories(user_option.weight, exercise_duration)
        try:
            user_record = UserDailyRecord.objects.get(
                Q(user_id=user) & Q(exercise_date=exercise_date)
            )
        except ObjectDoesNotExist:
            user_record = UserDailyRecord.objects.create(
                user_id=user,
                calories_total=calories,
                exercise_date=exercise_date,
                exercise_duration=exercise_duration,
            )
            return user_record
        user_record.calories_total += calories
        user_record.exercise_duration += exercise_duration
        user_record.save()
        return user_record


class UserMonthlyRecordSerializer(serializers.ModelSerializer):
    month_exercise_time = serializers.SerializerMethodField()
    month_calories = serializers.SerializerMethodField()
    records = UserDailyRecordSerializer(source="daily_record", many=True)

    def get_month_exercise_time(self, obj):
        time = list(obj.daily_record.aggregate(Sum("exercise_duration")).values())[0]
        return round(int(time) / 60) if time else 0

    def get_month_calories(self, obj):
        cals = list(obj.daily_record.aggregate(Sum("calories_total")).values())[0]
        return cals if cals else 0

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "nickname",
            "month_exercise_time",
            "month_calories",
            "records",
        )


class UserAnnualRecordSerializer(serializers.ModelSerializer):
    year_exercise_duration = serializers.SerializerMethodField()
    year_calories = serializers.SerializerMethodField()
    months_exercise_duration = serializers.SerializerMethodField()

    def get_year_exercise_duration(self, obj):
        time = list(obj.daily_record.aggregate(Sum("exercise_duration")).values())[0]
        return round(int(time) / 60) if time else 0

    def get_year_calories(self, obj):
        cals = list(obj.daily_record.aggregate(Sum("calories_total")).values())[0]
        return cals if cals else 0

    def get_months_exercise_duration(self, obj):
        time = list(
            obj.daily_record.annotate(month=F("exercise_date__month"))
            .values("month")
            .annotate(total=Sum("exercise_duration"))
        )
        return round(time / 60)

    def get_months_calories(self, obj):
        cals = list(
            obj.daily_record.annotate(month=F("exercise_date__month"))
            .values("month")
            .annotate(total=Sum("calories_total"))
        )
        return cals

    class Meta:
        model = User
        read_only_fields = ("nickname",)
        fields = (
            "id",
            "email",
            "nickname",
            "year_exercise_duration",
            "year_calories",
            "months_exercise_duration",
            "months_calories",
        )


class DateCheckSerializer(serializers.Serializer):
    month = serializers.IntegerField(min_value=1, max_value=12)
