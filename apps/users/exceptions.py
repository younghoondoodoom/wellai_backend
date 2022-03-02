from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import APIException


class InvalidDateException(APIException):
    status_code = 400
    default_detail = {"message": ["정확한 연도, 월을 입력해 주세요."]}
    default_code = _("쿼리 인풋값 에러")
