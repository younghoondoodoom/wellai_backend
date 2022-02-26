from django.urls import path

from .views import BookMarkListCreateView

urlpatterns = [
    path("bookmark", BookMarkListCreateView.as_view(), name="course-bookmark"),
]
