from rest_framework import generics, permissions

from apps.cores.paginations import StandardPageNumberPagination

from .models import Exercise
from .serializers import ExerciseSerializer

# Create your views here.


class ExerciseDetailView(generics.RetrieveAPIView):
    """
    운동 상세
    """

    name = "Exercise Detail"
    serializer_class = ExerciseSerializer
    pagination_class = StandardPageNumberPagination
    permission_classes = [permissions.IsAuthenticated]
    throttle_scope = "standard"
    queryset = Exercise.objects.all()
