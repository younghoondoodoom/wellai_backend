from django.core.validators import RegexValidator, ValidationError
from django.db import IntegrityError
from django.utils.translation import gettext_lazy as _


class NicknameValidator(RegexValidator):
    regex = r"^[가-힣a-zA-Z]+$"
    message = _("아이디 형식이 맞지 않습니다")


class PasswordValidator(RegexValidator):
    regex = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"
    message = _("비밀번호 형식이 맞지 않습니다")
