from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import APIException


class ReviewExistException(APIException):
    status_code = 400
    default_detail = {"review": ["이미 이 코스에 대한 리뷰가 있습니다!"]}
    default_code = _("댓글 중복")


class BookMarkExistException(APIException):
    status_code = 400
    default_detail = {"bookmark": ["이미 이 코스를 북마크 하셨습니다!"]}
    default_code = _("북마크 중복")
