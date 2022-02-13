import os

from django.urls import include, path

from .views import (
    CourseDetailAV,
    CourseListAV,
    ExerciseDetailAV,
    ReviewDeleteUpdateAV,
    ReviewListCreateAV,
)

urlpatterns = [
    # test api
    path("exercise/<int:pk>", ExerciseDetailAV.as_view(), name="exercise-detail"),
    path("list", CourseListAV.as_view(), name="course-list"),
    path("<int:pk>", CourseDetailAV.as_view(), name="course-detail"),
    path("<int:pk>/review", ReviewListCreateAV.as_view(), name="course-review"),
    path(
        "review/<int:pk>", ReviewDeleteUpdateAV.as_view(), name="review-update-destroy"
    ),
]
