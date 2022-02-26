from rest_framework import serializers

from .models import CourseReview


class CourseReviewSerializer(serializers.ModelSerializer):
    user_id = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = CourseReview
        exclude = ["is_deleted", "deleted_at"]
