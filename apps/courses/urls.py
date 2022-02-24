from django.urls import path

from .views import (
    BookMarkDeleteAV,
    BookMarkListCreateAV,
    CourseDetailAV,
    CourseListAV,
    ExerciseDetailAV,
    ReviewDeleteUpdateAV,
    ReviewListCreateAV,
)

urlpatterns = [
    path("exercise/<int:pk>", ExerciseDetailAV.as_view(), name="exercise-detail"),
    path("list", CourseListAV.as_view(), name="course-list"),
    path("<int:pk>", CourseDetailAV.as_view(), name="course-detail"),
    path("<int:pk>/review", ReviewListCreateAV.as_view(), name="review-list-create"),
    path(
        "review/<int:pk>", ReviewDeleteUpdateAV.as_view(), name="review-update-delete"
    ),
    path("bookmark", BookMarkListCreateAV.as_view(), name="course-bookmark"),
    path(
        "bookmark/<int:pk>", BookMarkDeleteAV.as_view(), name="course-bookmark-delete"
    ),
]
