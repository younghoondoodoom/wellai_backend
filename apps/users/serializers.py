from rest_framework import serializers

from .models import User, UserInfo, UserOption


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        exclude = ("user_id", "modified_at")


class UserOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserOption
        exclude = ("user_id", "modified_at")


class UserRegisterSerializer(serializers.ModelSerializer):
    option = UserOptionSerializer(source="user_option")

    class Meta:
        model = User
        fields = ("user_id", "nickname", "password", "option")


class UserDetailSerializer(serializers.ModelSerializer):
    daily_info = UserInfoSerializer(source="info", many=True)
    options = UserOptionSerializer(source="option")

    class Meta:
        model = User
        fields = ("id", "user_id", "nickname", "daily_info", "options")
