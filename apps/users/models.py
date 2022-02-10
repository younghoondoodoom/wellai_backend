import uuid

from django.contrib.auth.models import AbstractBaseUser
from django.db import models


class User(AbstractBaseUser):
    """
    - AbstractBaseUser
    password = models.CharField(_('password'), max_length=128)
    last_login = models.DateTimeField(_('last login'), blank=True, null=True)
    is_active = True
    """

    user_id = models.EmailField(unique=True, verbose_name="userid")
    nickname = models.CharField(max_length=64, verbose_name="nickname")
    uid = models.UUIDField(
        unique=True,
        editable=False,
        default=uuid.uuid4,
        verbose_name="public identifier",
    )
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True, editable=False)

    USERNAME_FIELD = "user_id"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.user_id
