import random

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import EmailValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from faker import Faker

from apps.cores.models import DeleteModel, TimeStampModel

from .validators import PasswordValidator


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")

        email = self.normalize_email(email)
        extra_fields.setdefault("is_superuser", False)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")

        email = self.normalize_email(email)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("nickname", "admin")
        superuser = self.model(email=email, **extra_fields)
        superuser.set_password(password)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        superuser.save()
        return superuser


class User(AbstractBaseUser, PermissionsMixin, TimeStampModel, DeleteModel):
    """
    - AbstractBaseUser : password, last_login, is_active
    - PermissionsMixin : is_superuser, groups, user_permissions
    - TimeStampModel : created_at, modified_at
    - DeleteModel : is_deleted, deleted_at
    """

    def set_nickname():
        fake = Faker(["ko_KR"])
        while True:
            try:
                nickname = fake.bs().split(" ")[0]
                nickname += random.choice(
                    [fake.first_name(), fake.job().split(" ")[-1]]
                )
                User.object.get(nickname=nickname)
            except Exception:
                return nickname

    email = models.EmailField(
        unique=True, validators=[EmailValidator()], verbose_name="이메일"
    )
    password = models.CharField(
        _("password"),
        max_length=128,
        validators=[PasswordValidator()],
    )
    nickname = models.CharField(
        unique=True,
        max_length=64,
        default=set_nickname,
        verbose_name="닉네임",
    )
    is_staff = models.BooleanField(default=False, verbose_name="관리자여부")

    USERNAME_FIELD = "email"
    objects = CustomUserManager()

    def __str__(self):
        return self.email
