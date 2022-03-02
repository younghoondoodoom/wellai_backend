from django.utils.translation import gettext_lazy as _
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
