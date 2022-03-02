from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, mixins, permissions, status
from rest_framework.response import Response

from apps.cores.permissions import IsOwner
from apps.users.exceptions import EmailExistException, PasswordCheckException

from .models import User, UserOption
from .serializers import (
    UserOptionSerializer,
    UserRegisterCheckSerializer,
    UserRegisterSerializer,
)


class UserRegisterCheckView(generics.CreateAPIView):
    serializer_class = UserRegisterCheckSerializer

    def post(self, request, *args, **kwargs):
        if request.data["password"] != request.data["confirm_password"]:
            raise PasswordCheckException()

        serializer = UserRegisterCheckSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            User.objects.get(email=request.data["email"])
            raise EmailExistException()
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_200_OK)


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
