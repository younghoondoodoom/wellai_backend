from django.core.validators import EmailValidator
from django.db.models import Sum
from rest_framework import serializers

from .models import User, UserDailyRecord, UserOption
from .validators import PasswordValidator


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


class UserDailyRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDailyRecord
        fields = "__all__"


class UserWeeklyRecordSerializer(serializers.ModelSerializer):
    records = UserDailyRecordSerializer(source="daily_record", many=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "nickname",
            "records",
        )


class UserMonthlyRecordSerializer(serializers.ModelSerializer):
    month_exercise_time = serializers.SerializerMethodField()
    month_calories = serializers.SerializerMethodField()

    def get_month_exercise_time(self, obj):
        time = list(obj.daily_record.aggregate(Sum("exercise_duration")).values())[0]
        return int(time) if time else 0

    def get_month_calories(self, obj):
        cals = list(obj.daily_record.aggregate(Sum("calories_total")).values())[0]
        return cals if cals else 0

    class Meta:
        model = User
        read_only_fields = ("nickname",)
        fields = (
            "id",
            "email",
            "nickname",
            "month_exercise_time",
            "month_calories",
        )


class DateCheckSerializer(serializers.Serializer):
    year = serializers.IntegerField()
    month = serializers.IntegerField(min_value=1, max_value=12)
