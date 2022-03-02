from django.urls import path

from .views import (
    CourseDetailView,
    CourseListView,
    ExerciseDetailView,
    ReviewDeleteUpdateView,
    ReviewListCreateView,
)

urlpatterns = [
    path("exercise/<int:pk>", ExerciseDetailView.as_view(), name="exercise-detail"),
    path("list", CourseListView.as_view(), name="course-list"),
    path("<int:pk>", CourseDetailView.as_view(), name="course-detail"),
    path("<int:pk>/review", ReviewListCreateView.as_view(), name="review-list-create"),
    path(
        "review/<int:pk>", ReviewDeleteUpdateView.as_view(), name="review-update-delete"
    ),
]
