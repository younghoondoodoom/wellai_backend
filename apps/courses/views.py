from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Course, Exercise
from .serializers import CourseSerializer, ExerciseSerializer

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
