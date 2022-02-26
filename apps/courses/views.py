from rest_framework import filters, generics, permissions

from apps.cores.paginations import StandardPageNumberPagination

from .models import Course, Exercise
from .serializers import CourseSerializer, ExerciseSerializer


class ExerciseDetailView(generics.RetrieveAPIView):
    """
    운동 상세
    """

    name = "Exercise Detail"
    serializer_class = ExerciseSerializer
    pagination_class = StandardPageNumberPagination
    permission_classes = [permissions.IsAuthenticated]
    throttle_scope = "standard"
    queryset = Exercise.objects.all()


class CourseListView(generics.ListAPIView):
    """
    코스 리스트(검색 기능 포함)
    """

    name = "Course List"
    serializer_class = CourseSerializer
    pagination_class = StandardPageNumberPagination
    permission_classes = [permissions.AllowAny]
    throttle_scope = "standard"
    queryset = Course.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ["course_name", "hash_tag__tag"]


class CourseDetailView(generics.RetrieveAPIView):
    """
    코스의 상세정보(리뷰 미포함)
    """

    name = "Course Detail"
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_scope = "standard"
    queryset = Course.objects.all()
