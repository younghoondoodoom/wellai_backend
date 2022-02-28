from rest_framework import generics, permissions

from apps.users.models import UserOption

from .models import Course
from .serializers import CourseSerializer


class CourseRecommendView(generics.ListAPIView):
    """
    코스 추천
    """

    name = "Course Recommendation"
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_scope = "standard"

    def get_queryset(self):
        user = self.request.user
        user_option = user.option
        course = Course.objects.all()
        queryset = None
        if user_option.stand:  # must fix: model 변경 후 반드시 수정
            queryset = course.order_by("-stand_count")[:5]
        if user_option.sit:
            qs = course.order_by("-sit_count")[:5]
            if queryset is None:
                queryset = qs
            else:
                queryset = queryset | qs
        if user_option.balance:
            qs = course.order_by("-balance_count")[:5]
            if queryset is None:
                queryset = qs
            else:
                queryset = queryset | qs
        if user_option.core:
            qs = course.order_by("-core_count")[:5]
            if queryset is None:
                queryset = qs
            else:
                queryset = queryset | qs
        if user_option.leg:
            qs = course.order_by("-leg_count")[:5]
            if queryset is None:
                queryset = qs
            else:
                queryset = queryset | qs
        if user_option.back:
            qs = course.order_by("-back_count")[:5]
            if queryset is None:
                queryset = qs
            else:
                queryset = queryset | qs

        if queryset is None:
            return course.order_by("?")

        return queryset.order_by("?")[0:1]
