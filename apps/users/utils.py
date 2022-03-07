import random

import jwt
from config.settings.base import SIMPLE_JWT
from django.core.exceptions import ObjectDoesNotExist
from faker import Faker


def get_calories(weight, duration):
    # 식 : MET(요가 에너지소비량) x Weight(몸무게)  x 0.0175 x Time(min) = Kcal
    return 3.1 * weight * 0.0175 * duration


def get_decoded_token(token):
    options = {
        "verify_signature": False,
        "verify_aud": False,
        "require_sub": True,
    }
    decoded_token = jwt.decode(
        token,
        SIMPLE_JWT["SIGNING_KEY"],
        algorithms=[SIMPLE_JWT["ALGORITHM"]],
        options=options,
    )
    return decoded_token


def get_nickname():
    from apps.users.models import User

    fake = Faker(["ko_KR"])
    while True:
        nickname = fake.bs().split(" ")[0]
        nickname += random.choice([fake.first_name(), fake.job().split(" ")[-1]])
        try:
            User.objects.get(nickname=nickname)
        except Exception:
            return nickname
