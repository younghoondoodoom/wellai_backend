from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class PasswordValidator(RegexValidator):
    regex = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"
    message = _("비밀번호 형식이 맞지 않습니다")
