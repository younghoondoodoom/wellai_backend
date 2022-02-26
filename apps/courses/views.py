from rest_framework import filters, generics, permissions
from rest_framework.exceptions import ValidationError

from apps.cores.paginations import StandardPageNumberPagination
from apps.cores.permissions import IsOwner

from .models import Course, CourseReview
from .serializers import CourseReviewSerializer


class ReviewListCreateView(generics.ListCreateAPIView):
    """
    코스 리뷰 리스트 및 생성(정렬 기능 포함)
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

    def perform_create(self, serializer):
        """
        코스 평균 평점에 리뷰 평점을 반영
        """
        course_id = self.kwargs.get("pk")
        course = Course.objects.get(pk=course_id)

        user = self.request.user
        review_queryset = CourseReview.objects.filter(course_id=course, user_id=user)

        if review_queryset.exists():
            raise ("이미 이 코스에 대한 리뷰가 있습니다!")

        if course.count_review == 0:
            course.avg_rating = serializer.validated_data["rating"]

        else:
            course.avg_rating = round(
                (course.avg_rating + serializer.validated_data["rating"]) / 2, 1
            )

        course.count_review += 1
        course.save()

        serializer.save()


class ReviewDeleteUpdateView(generics.RetrieveUpdateDestroyAPIView):
    """
    코스 리뷰 삭제 및 업데이트
    """

    name = "Course Review Read & Update & Delete"
    serializer_class = CourseReviewSerializer
    permission_classes = [IsOwner]
    throttle_scope = "standard"
    queryset = CourseReview.objects.all()
