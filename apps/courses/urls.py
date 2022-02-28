from django.urls import path

from .views import CourseRecommendView

urlpatterns = [
    path("recommendation", CourseRecommendView.as_view(), name="course-recommend"),
]
