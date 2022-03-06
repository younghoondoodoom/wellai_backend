import jwt
from config.settings.base import SIMPLE_JWT


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
