from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import APIException


class PasswordCheckException(APIException):
    status_code = 400
    default_detail = {"password": ["비밀번호가 일치하지 않습니다."]}
    default_code = _("비밀번호 불일치")


class EmailExistException(APIException):
    status_code = 400
    default_detail = {"email": ["존재하는 아이디입니다."]}
    default_code = _("이메일 중복")
