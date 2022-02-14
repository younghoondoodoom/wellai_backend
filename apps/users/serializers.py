from rest_framework import serializers

from .models import User, UserDailyInfo, UserOption


class UserDailyInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDailyInfo
        exclude = ("user_id", "modified_at")


class UserOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserOption
        exclude = ("user_id", "modified_at")


class UserRegisterSerializer(serializers.ModelSerializer):
    options = UserOptionSerializer(source="user_option")

    class Meta:
        model = User
        fields = ("user_id", "nickname", "password", "options")


class UserDetailSerializer(serializers.ModelSerializer):
    daily = UserDailyInfoSerializer(source="daily_info", many=True)
    options = UserOptionSerializer(source="option")

    class Meta:
        model = User
        fields = ("id", "user_id", "nickname", "daily", "options")
