from django.urls import path

from .views import ReviewDeleteUpdateView, ReviewListCreateView

urlpatterns = [
    path("<int:pk>/review", ReviewListCreateView.as_view(), name="review-list-create"),
    path(
        "review/<int:pk>", ReviewDeleteUpdateView.as_view(), name="review-update-delete"
    ),
]
