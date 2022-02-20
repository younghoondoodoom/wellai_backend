from django.core.validators import EmailValidator
from rest_framework import serializers

from .models import User, UserDailyInfo, UserOption
from .validators import NicknameValidator, PasswordValidator


class UserSerializer(serializers.Serializer):
    user_id = serializers.EmailField(validators=[EmailValidator()])
    nickname = serializers.CharField(
        max_length=64, min_length=2, validators=[NicknameValidator()]
    )
    password = serializers.CharField(
        max_length=128, min_length=8, validators=[PasswordValidator()]
    )
    password2 = serializers.CharField(
        max_length=128, min_length=8, validators=[PasswordValidator()]
    )

    def validate(self, attrs):
        password = attrs["password"]
        password2 = attrs["password2"]
        if password != password2:
            raise serializers.ValidationError(detail="비밀번호가 일치하지 않습니다.")
        return attrs

    def validate_user_id(self, attr):
        user_id = attr
        try:
            User.objects.get(user_id=user_id)
        except Exception:
            return attr
        raise serializers.ValidationError(detail="존재하는 아이디입니다.")

    def validate_nickname(self, attr):
        nickname = attr
        try:
            User.objects.get(nickname=nickname)
        except Exception:
            return attr
        raise serializers.ValidationError(detail="존재하는 닉네임입니다.")


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
