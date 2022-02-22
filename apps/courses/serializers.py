from rest_framework import serializers

from .models import Course, CourseLike, CourseReview, Exercise, Tag


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
        fields = "__all__"


class CourseReviewSerializer(serializers.ModelSerializer):
    user_id = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = CourseReview
        exclude = ["is_deleted", "deleted_at"]


class CourseLikeSerializer(serializers.ModelSerializer):
    user_id = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = CourseLike
        fields = "__all__"
