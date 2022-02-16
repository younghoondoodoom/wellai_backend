from django.utils.translation import gettext_lazy as _
from rest_framework import filters, generics, permissions, status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.response import Response

from apps.cores.paginations import StandardPageNumberPagination
from apps.cores.permissions import IsOwner

from .models import Course, CourseReview, Exercise
from .serializers import CourseReviewSerializer, CourseSerializer, ExerciseSerializer

# Create your views here.


class ExerciseDetailAV(generics.RetrieveAPIView):
    """
    운동 상세
    """

    name = "Exercise Detail"
    serializer_class = ExerciseSerializer
    pagination_class = StandardPageNumberPagination
    permission_classes = [permissions.IsAuthenticated]
    throttle_scope = "standard"
    queryset = Exercise.objects.all()


class CourseListAV(generics.ListAPIView):
    """
    코스 리스트
    """

    name = "Course List"
    serializer_class = CourseSerializer
    pagination_class = StandardPageNumberPagination
    permission_classes = [permissions.AllowAny]
    throttle_scope = "standard"
    queryset = Course.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ["course_name", "hash_tag__tag"]


class CourseDetailAV(generics.RetrieveAPIView):
    """
    코스의 상세정보(리뷰 미포함)
    """

    name = "Course Detail"
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_scope = "standard"
    queryset = Course.objects.all()


class ReviewListCreateAV(generics.ListCreateAPIView):
    """
    코스 리뷰 리스트 및 생성
    """

    name = "Course Review List & Create"
    serializer_class = CourseReviewSerializer
    pagination_class = StandardPageNumberPagination
    throttle_scope = "standard"
    permission_classes = [permissions.IsAuthenticated]
    queryset = CourseReview.objects.all()
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["rating", "created_at"]
    ordering = ["-rating"]

    def create(self, request, *args, **kwargs):
        context = {
            "request": self.request,
        }
        serializer = self.get_serializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        """
        코스 평균 평점에 리뷰 평점을 반영
        """
        pk = self.kwargs.get("pk")
        course = Course.objects.get(pk=pk)

        user = self.request.user
        review_queryset = CourseReview.objects.filter(course_id=course, user_id=user)

        if review_queryset.exists():
            raise ValidationError("이미 이 코스에 대한 리뷰가 있습니다!")

        if course.count_review == 0:
            course.avg_rating = serializer.validated_data["rating"]

        else:
            course.avg_rating = round(
                (course.avg_rating + serializer.validated_data["rating"]) / 2, 1
            )

        course.count_review += 1
        course.save()

        serializer.save()


class ReviewDeleteUpdateAV(generics.RetrieveUpdateDestroyAPIView):
    """
    코스 리뷰 삭제 및 업데이트
    """

    name = "Course Review Read & Update & Destroy"
    serializer_class = CourseReviewSerializer
    permission_classes = [IsOwner]
    throttle_scope = "standard"
    queryset = CourseReview.objects.all()
