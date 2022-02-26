from django.urls import path

from .views import CourseListView, ExerciseDetailView

urlpatterns = [
    path("exercise/<int:pk>", ExerciseDetailView.as_view(), name="exercise-detail"),
    path("list", CourseListView.as_view(), name="course-list"),
]
