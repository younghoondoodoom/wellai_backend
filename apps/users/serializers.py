from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

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


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["user_id"] = user.user_id
        return token
