from rest_framework import serializers

from .models import Course, CourseReview, Exercise


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    exercises = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="exercise-detail"
    )

    class Meta:
        model = Course
        fields = "__all__"


class CourseReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseReview
        fields = "__all__"
