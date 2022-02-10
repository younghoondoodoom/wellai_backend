from rest_framework import serializers

from .models import Exercise, Course

class ExerciseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Exercise
        fields = '__all__'
        

class CourseSerializer(serializers.ModelSerializer):
    exercises = ExerciseSerializer(many=True, read_only=True)
    
    class Meta:
        model = Course
        fields = '__all__'