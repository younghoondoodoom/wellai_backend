from django.urls import path

from .views import (
    BookMarkDeleteView,
    BookMarkListCreateView,
    CourseDetailView,
    CourseListView,
    CourseRecommendView,
    ExerciseDetailView,
    MyReviewCollectListView,
    MyReviewListView,
    ReviewDeleteUpdateView,
    ReviewListCreateView,
)

urlpatterns = [
    path("exercise/<int:pk>", ExerciseDetailView.as_view(), name="exercise-detail"),
    path("list", CourseListView.as_view(), name="course-list"),
    path("<int:pk>", CourseDetailView.as_view(), name="course-detail"),
    path("<int:pk>/review", ReviewListCreateView.as_view(), name="review-list-create"),
    path(
        "review/collection", MyReviewCollectListView.as_view(), name="review-collection"
    ),
    path("<int:pk>/myreview", MyReviewListView.as_view(), name="myreview-retrieve"),
    path(
        "review/<int:pk>", ReviewDeleteUpdateView.as_view(), name="review-update-delete"
    ),
    path("bookmark", BookMarkListCreateView.as_view(), name="course-bookmark"),
    path(
        "bookmark/<int:pk>", BookMarkDeleteView.as_view(), name="course-bookmark-delete"
    ),
    path("recommendation", CourseRecommendView.as_view(), name="course-recommend"),
]
