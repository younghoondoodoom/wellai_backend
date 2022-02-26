from django.urls import path

from .views import BookMarkDeleteView, BookMarkListCreateView

urlpatterns = [
    path("bookmark", BookMarkListCreateView.as_view(), name="course-bookmark"),
    path(
        "bookmark/<int:pk>", BookMarkDeleteView.as_view(), name="course-bookmark-delete"
    ),
]
