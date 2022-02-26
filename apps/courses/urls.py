from django.urls import path

from .views import CourseDetailView, CourseListView, ExerciseDetailView

urlpatterns = [
    path("exercise/<int:pk>", ExerciseDetailView.as_view(), name="exercise-detail"),
    path("list", CourseListView.as_view(), name="course-list"),
    path("<int:pk>", CourseDetailView.as_view(), name="course-detail"),
]
