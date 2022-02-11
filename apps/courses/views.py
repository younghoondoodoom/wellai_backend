from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from apps.cores.paginations import StandardPageNumberPagination

from .models import Course, CourseReview, Exercise
from .serializers import CourseReviewSerializer, CourseSerializer, ExerciseSerializer

# Create your views here.


class ExerciseDetailAV(generics.RetrieveAPIView):
    """
    운동 리스트
    """

    name = "Exercise Detail"
    serializer_class = ExerciseSerializer
    pagination_class = PageNumberPagination
    queryset = Exercise.objects.all()


class CourseListAV(generics.ListAPIView):
    """
    코스 리스트
    """

    name = "Course List"
    serializer_class = CourseSerializer
    pagination_class = StandardPageNumberPagination
    queryset = Course.objects.all()


class CourseDetailAV(generics.RetrieveAPIView):
    """
    코스의 상세정보(리뷰 미포함)
    """

    name = "Course Detail"
    serializer_class = CourseSerializer
    queryset = Course.objects.all()


class ReviewListCreateAV(generics.ListCreateAPIView):
    """
    코스 리뷰 리스트 및 생성
    """

    name = "Course Review Create"
    serializer_class = CourseReviewSerializer
    pagination_class = StandardPageNumberPagination
    queryset = CourseReview.objects.all()


class ReviewDeleteUpdateAV(generics.DestroyAPIView, generics.UpdateAPIView):
    """
    코스 리뷰 삭제 및 업데이트
    """

    name = "Course Review Delete Update"
    serializer_class = CourseReviewSerializer
    queryset = CourseReview.objects.all()
