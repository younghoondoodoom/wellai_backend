from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError

from apps.cores.permissions import IsOwner

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
        queryset = user.user_bookmark.all()
        return queryset

    def perform_create(self, serializer):
        course = serializer.validated_data["course_id"]
        user = self.request.user
        bookmark_queryset = user.user_bookmark.filter(course_id=course)

        if bookmark_queryset.exists():
            raise ValidationError("이미 이 코스를 북마크 하셨습니다!")

        serializer.save()


class BookMarkDeleteView(generics.DestroyAPIView):
    """
    북마크 삭제
    """

    name = "Course Bookmark Delete"
    serializer = BookMarkSerializer
    permission_classes = [IsOwner]
    throttle_scope = "standard"
    queryset = BookMark.objects.all()
