from django.core.validators import EmailValidator
from rest_framework import serializers

from .models import User, UserDailyRecord, UserOption
from .validators import PasswordValidator


class UserOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserOption
        fields = "__all__"
        read_only_fields = ("id", "user_id", "modified_at", "created_at")


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
        useroption = options_serializer.create(options_validated_data)
        return user
