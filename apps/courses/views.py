from django.db import transaction
from django.utils.translation import gettext_lazy as _
from rest_framework import filters, generics, permissions, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from apps.cores.paginations import StandardPageNumberPagination
from apps.cores.permissions import IsOwnerProp

from .exceptions import (
    BookmarkDeleteException,
    BookMarkExistException,
    ReviewExistException,
)
from .models import BookMark, Course, CourseReview, Exercise
from .serializers import (
    BookmarkCreateSerializer,
    BookMarkSerializer,
    CourseReviewSerializer,
    CourseReviewShowCourseSerializer,
    CourseReviewShowUserSerializer,
    CourseSerializer,
    ExerciseSerializer,
)


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
    search_fields = ["course_name", "hash_tag__tag_name"]


class CourseDetailView(generics.RetrieveAPIView):
    """
    코스의 상세정보(리뷰 미포함)
    """

    name = "Course Detail"
    serializer_class = CourseSerializer
    permission_classes = [permissions.AllowAny]
    throttle_scope = "standard"
    queryset = Course.objects.all()


class ReviewListCreateView(generics.ListCreateAPIView):
    """
    코스 리뷰 리스트 및 생성(정렬 기능 포함)
    """

    name = "Course Review List & Create"
    serializer_class = CourseReviewShowUserSerializer
    pagination_class = StandardPageNumberPagination
    throttle_scope = "standard"
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["rating", "created_at"]
    ordering = ["-rating"]

    def get_queryset(self):
        try:
            course = Course.objects.get(pk=self.kwargs.get("pk"))
        except Course.DoesNotExist:
            raise NotFound
        course_review = course.review
        return course_review

    def get_permissions(self):
        if self.request.method == "POST":
            self.permission_classes = [permissions.IsAuthenticated]
        self.permission_classes = [permissions.AllowAny]
        return super(self.__class__, self).get_permissions()

    @transaction.atomic
    def perform_create(self, serializer):
        """
        코스 평균 평점, 평점 개수에 셍성되는 리뷰를 반영
        """
        course = serializer.validated_data["course_id"]
        user = self.request.user
        review_queryset = user.review.filter(course_id=course)

        if review_queryset.exists():
            raise ReviewExistException

        if course.count_review == 0:
            course.avg_rating = serializer.validated_data["rating"]
        else:
            course.avg_rating = round(
                (course.avg_rating + serializer.validated_data["rating"]) / 2, 1
            )

        course.count_review += 1
        course.save()

        serializer.save(user_id=user, course_id=course)


class MyReviewCollectListView(generics.ListAPIView):
    """
    유저의 댓글 모음
    """

    name = "Review Collect List"
    serializer_class = CourseReviewShowCourseSerializer
    permission_classes = [IsOwnerProp]
    throttle_scope = "standard"

    def get_queryset(self):
        user = self.request.user
        review_queryset = user.review
        return review_queryset


class MyReviewListView(generics.ListAPIView):
    """
    유저가 해당 코스에 작성한 댓글
    """

    name = "MyReview In The Course"
    serializer_class = CourseReviewShowUserSerializer
    permission_classes = [IsOwnerProp]
    throttle_scope = "standard"
    queryset = CourseReview.objects.all()

    def filter_queryset(self, queryset):
        queryset = queryset.filter(
            course_id=self.kwargs.get("pk"), user_id=self.request.user
        )
        return queryset


class ReviewDeleteUpdateView(generics.RetrieveUpdateDestroyAPIView):
    """
    코스 리뷰 삭제 및 업데이트
    """

    name = "Course Review Read & Update & Delete"
    serializer_class = CourseReviewSerializer
    permission_classes = [IsOwnerProp]
    throttle_scope = "standard"
    queryset = CourseReview.objects.all()

    @transaction.atomic
    def perform_destroy(self, review):
        """
        코스 평균 평점, 리뷰 개수에 삭제되는 리뷰를 반영
        """
        course = review.course_id
        count_review = course.count_review

        if count_review == 1:
            course.avg_rating = 0
        else:
            course.avg_rating = round(
                (course.avg_rating * count_review - review.rating) / (count_review - 1),
                1,
            )
        course.count_review -= 1
        course.save()

        review.delete()

    @transaction.atomic
    def perform_update(self, serializer):
        """
        코스 평균 평점에 수정되는 리뷰를 반영
        """
        review = self.get_object()
        course = review.course_id
        count_review = course.count_review

        if count_review == 1:
            course.avg_rating = serializer.validated_data["rating"]
        else:
            course.avg_rating = round(
                (
                    course.avg_rating * count_review
                    - review.rating
                    + serializer.validated_data["rating"]
                )
                / count_review
            )
        course.save()

        serializer.save()


class BookMarkListCreateView(generics.ListCreateAPIView):
    """
    북마크 생성, 조회
    """

    name = "Course BookMark List Create"
    permission_classes = [permissions.IsAuthenticated]
    throttle_scope = "standard"

    def get_serializer_class(self):
        if self.request.method == "POST":
            return BookmarkCreateSerializer
        return BookMarkSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = user.bookmark.all()
        queryset = queryset.order_by("created_at")
        return queryset

    @transaction.atomic
    def perform_create(self, serializer):
        course = serializer.validated_data["course_id"]
        user = self.request.user
        bookmark_queryset = user.bookmark.filter(course_id=course)

        if bookmark_queryset.exists():
            raise BookMarkExistException

        serializer.save()


class BookMarkDeleteView(generics.DestroyAPIView):
    """
    북마크 삭제
    """

    name = "Course Bookmark Delete"
    serializer = BookMarkSerializer
    permission_classes = [IsOwnerProp]
    throttle_scope = "standard"
    queryset = BookMark.objects.all()

    def destroy(self, request, *args, **kwargs):
        try:
            bookmark = self.queryset.get(
                course_id=self.kwargs.get("pk"), user_id=request.user
            )
        except BookMark.DoesNotExist:
            raise BookmarkDeleteException
        self.perform_destroy(bookmark)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CourseRecommendView(generics.ListAPIView):
    """
    코스 추천
    """

    name = "Course Recommendation"
    serializer_class = CourseSerializer
    permission_classes = [permissions.AllowAny]
    throttle_scope = "standard"

    def list(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return Response(status=status.HTTP_204_NO_CONTENT)
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        user = self.request.user
        user_option = user.option
        course = Course.objects.all()
        queryset = None
        if user_option.is_stand:
            queryset = course.order_by("-stand_count")[:5]
        if user_option.is_sit:
            qs = course.order_by("-sit_count")[:5]
            if queryset is None:
                queryset = qs
            else:
                queryset = queryset | qs
        if user_option.is_balance:
            qs = course.order_by("-balance_count")[:5]
            if queryset is None:
                queryset = qs
            else:
                queryset = queryset | qs
        if user_option.is_core:
            qs = course.order_by("-core_count")[:5]
            if queryset is None:
                queryset = qs
            else:
                queryset = queryset | qs
        if user_option.is_leg:
            qs = course.order_by("-arm_count")[:5]
            if queryset is None:
                queryset = qs
            else:
                queryset = queryset | qs
        if user_option.is_back:
            qs = course.order_by("-recline_count")[:5]
            if queryset is None:
                queryset = qs
            else:
                queryset = queryset | qs

        if queryset is None:
            return course.order_by("?")

        return queryset.order_by("?")[0:1]
