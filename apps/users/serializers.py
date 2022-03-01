from django.core.validators import EmailValidator
from rest_framework import serializers

from .models import User, UserOption
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

    class Meta:
        model = User
        read_only_fields = ("nickname",)
        fields = ("email", "nickname", "password", "options")
