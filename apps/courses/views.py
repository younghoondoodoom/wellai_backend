from django.db import transaction
from django.db.models import Avg, Count
from django.utils.translation import gettext_lazy as _
from rest_framework import filters, generics, permissions, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from apps.cores.paginations import (
    CoursePageNumberPagination,
    ReviewPageNumberPagination,
)
from apps.cores.permissions import IsOwnerProp

from .exceptions import (
    BookmarkDeleteException,
    BookMarkExistException,
    ReviewExistException,
)
from .models import BookMark, Course, CourseReview, Exercise, Tag
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
    permission_classes = [permissions.IsAuthenticated]
    throttle_scope = "standard"
    queryset = Exercise.objects.all()


class CourseListView(generics.ListAPIView):
    """
    코스 리스트(검색 기능 포함)
    """

    name = "Course List"
    serializer_class = CourseSerializer
    pagination_class = CoursePageNumberPagination
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
    pagination_class = ReviewPageNumberPagination
    throttle_scope = "standard"
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["rating", "created_at"]
    ordering = ["-created_at"]

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

        serializer.save(user_id=user, course_id=course)

        reviews = course.review.filter(is_deleted=False).aggregate(
            Avg("rating"), Count("id")
        )
        course.avg_rating = round(reviews["rating__avg"], 1)
        course.count_review = reviews["id__count"]
        course.save()


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
        review.delete()

        course = review.course_id
        if course.review.count() == 0:
            course.avg_rating = 0
        else:
            reviews = course.review.filter(is_deleted=False).aggregate(
                Avg("rating"), Count("id")
            )
            course.avg_rating = round(reviews["rating__avg"], 1)
            course.count_review = reviews["id__count"]

        course.save()

    @transaction.atomic
    def perform_update(self, serializer):
        """
        코스 평균 평점에 수정되는 리뷰를 반영
        """
        serializer.save()

        review = self.get_object()
        course = review.course_id
        reviews = course.review.filter(is_deleted=False).aggregate(Avg("rating"))
        course.avg_rating = round(reviews["rating__avg"], 1)
        course.save()


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

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        user = self.request.user
        user_option = user.option
        queryset = None
        if user_option.is_stand:
            stand_tag = Tag.objects.get(tag_name="서서")
            queryset = stand_tag.course.all()
        if user_option.is_sit:
            sit_tag = Tag.objects.get(tag_name="앉아서")
            qs = sit_tag.course.all()
            if queryset is None:
                queryset = qs
            else:
                queryset = queryset | qs
        if user_option.is_balance:
            balance_tag = Tag.objects.get(tag_name="밸런스")
            qs = balance_tag.course.all()
            if queryset is None:
                queryset = qs
            else:
                queryset = queryset | qs
        if user_option.is_core:
            core_tag = Tag.objects.get(tag_name="코어")
            qs = core_tag.course.all()
            if queryset is None:
                queryset = qs
            else:
                queryset = queryset | qs
        if user_option.is_arm:
            arm_tag = Tag.objects.get(tag_name="팔")
            qs = arm_tag.course.all()
            if queryset is None:
                queryset = qs
            else:
                queryset = queryset | qs
        if user_option.is_recline:
            recline_tag = Tag.objects.get(tag_name="누워서")
            qs = recline_tag.course.all()
            if queryset is None:
                queryset = qs
            else:
                queryset = queryset | qs

        if queryset is None:
            return Course.objects.order_by("?")[0:1]

        return queryset.order_by("?")[0:1]
