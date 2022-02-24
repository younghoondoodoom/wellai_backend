import os

from .base import *  # noqa: F403, F401

# TODO: 차후 배포시 서버 호스트 기입 필요
DEBUG = False
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")
