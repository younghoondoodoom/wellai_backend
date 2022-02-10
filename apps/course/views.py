from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.pagination import PageNumberPagination

from .models import Exercise, Course
from .serializers import ExerciseSerializer, CourseSerializer
# Create your views here.

class ExerciseList(generics.ListAPIView):
    """
    test api
    """
    serializer_class = ExerciseSerializer
    pagination_class = PageNumberPagination
    queryset = Exercise.objects.all()
    

class ExerciseCourseList(generics.ListAPIView):
    """
    test api
    """
    serializer_class = CourseSerializer
    pagination_class = PageNumberPagination
    queryset = Course.objects.all()