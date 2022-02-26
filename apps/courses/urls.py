from django.urls import path

from .views import CourseRecommendView

urlpatterns = [
    path("recommend", CourseRecommendView.as_view(), name="course-recommend"),
]
