from rest_framework import serializers

from .models import Course, Exercise, Tag


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
