from rest_framework import serializers

from apps.users.models import User

from .models import BookMark, Course, CourseReview, Exercise, Tag


class TagSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        exclude = ["id"]


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    exercises = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="exercise-detail"
    )
    hash_tag = TagSerailizer(many=True, read_only=True)

    class Meta:
        model = Course
        exclude = [
            "stand_count",
            "sit_count",
            "balance_count",
            "core_count",
            "arm_count",
            "recline_count",
            "review_user",
            "bookmark_user",
        ]


class CourseReviewShowUserSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField(source="user_id.nickname")

    class Meta:
        model = CourseReview
        exclude = ["is_deleted", "deleted_at"]


class CourseReviewStandardSerializer(serializers.ModelSerializer):
    user_id = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = CourseReview
        exclude = ["is_deleted", "deleted_at", "course_id"]


class BookMarkSerializer(serializers.ModelSerializer):
    user_id = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = BookMark
        fields = "__all__"
