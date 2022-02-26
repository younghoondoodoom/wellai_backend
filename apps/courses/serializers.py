from rest_framework import serializers

from .models import BookMark


class BookMarkSerializer(serializers.ModelSerializer):
    user_id = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = BookMark
        fields = "__all__"
