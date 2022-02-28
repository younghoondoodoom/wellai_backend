from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, status
from rest_framework.response import Response

from apps.users.exceptions import EmailExistException, PasswordCheckException

from .models import User
from .serializers import UserRegisterCheckSerializer


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
