from django.urls import path

from .views import ExerciseDetailView

urlpatterns = [
    path("exercise/<int:pk>", ExerciseDetailView.as_view(), name="exercise-detail"),
]
