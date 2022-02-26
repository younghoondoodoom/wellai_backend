from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError

from .models import BookMark
from .serializers import BookMarkSerializer


class BookMarkListCreateView(generics.ListCreateAPIView):
    """
    북마크 생성, 조회
    """

    name = "Course BookMark Create"
    serializer_class = BookMarkSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_scope = "standard"

    def get_queryset(self):
        user = self.request.user
        queryset = BookMark.objects.filter(user_id=user)
        return queryset

    def perform_create(self, serializer):
        course_id = serializer.validated_data["course_id"]
        user = self.request.user
        bookmark_queryset = BookMark.objects.filter(user_id=user, course_id=course_id)

        if bookmark_queryset.exists():
            raise ValidationError("이미 이 코스를 북마크 하셨습니다!")

        serializer.save()
