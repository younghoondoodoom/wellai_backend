from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if response.data.get("detail") is None:
            for error in response.data:
                response.data[error] = response.data[error][0]
        else:
            response.data["message"] = response.data["detail"]
            del response.data["detail"]
        response.data["status_code"] = response.status_code
    return response


class PasswordCheckException(APIException):
    status_code = 400
    default_detail = {"password": ["비밀번호가 일치하지 않습니다."]}
    default_code = _("비밀번호 불일치")


class EmailExistException(APIException):
    status_code = 400
    default_detail = {"email": ["존재하는 아이디입니다."]}
    default_code = _("이메일 중복")
