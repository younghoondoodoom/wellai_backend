from rest_framework import generics, mixins, permissions, status
from rest_framework.response import Response

from apps.cores.permissions import IsOwner

from .models import User, UserOption
from .serializers import UserOptionSerializer, UserRegisterSerializer


class UserOptionUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsOwner]
    serializer_class = UserOptionSerializer
    queryset = UserOption.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = User.objects.get(id=request.user.id)
        serializer = UserRegisterSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = True
        instance = UserOption.objects.get_or_create(user_id=request.user)[0]
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data, status=status.HTTP_200_OK)
