import uuid

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, user_id, password, **extra_fields):
        if not user_id:
            raise ValueError("The given user_id must be set")

        user_id = self.normalize_email(user_id)
        extra_fields.setdefault("is_superuser", False)
        user = self.model(user_id=user_id, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, user_id, password, **extra_fields):
        if not user_id:
            raise ValueError("The given user_id must be set")

        user_id = self.normalize_email(user_id)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("nickname", "admin")
        superuser = self.model(user_id=user_id, **extra_fields)
        superuser.set_password(password)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        superuser.save()
        return superuser


class User(AbstractBaseUser, PermissionsMixin):
    """
    - AbstractBaseUser
    password, last_login, is_active

    - PermissionsMixin
    is_superuser, groups, user_permissions
    """

    user_id = models.EmailField(unique=True, verbose_name="userid")
    nickname = models.CharField(max_length=64, verbose_name="nickname")
    uid = models.UUIDField(
        unique=True,
        editable=False,
        default=uuid.uuid4,
        verbose_name="public identifier",
    )
    date_joined = models.DateTimeField(default=timezone.localtime, editable=False)
    is_deleted = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "user_id"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.user_id


class UserInfo(models.Model):
    user_id = models.ForeignKey(
        "User", related_name="user_info", on_delete=models.CASCADE, db_column="user_id"
    )
    exercise_total = models.IntegerField(default=0, verbose_name="일별 총 운동시간")
    calories_total = models.IntegerField(default=0, verbose_name="일별 총 소모칼로리")
    exercise_date = models.DateTimeField(
        unique=True, default=timezone.localdate, verbose_name="날짜"
    )
    # exercise_day = models.DateTimeField(default=, verbose_name="요일")
    modified_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f"{self.user_id}: {self.workout_day}mins, {self.calories_day}cals"


class UserOption(models.Model):
    GENDER_CHOICES = [
        ("F", "여"),
        ("M", "남"),
    ]
    user_id = models.ForeignKey(
        "User",
        related_name="user_option",
        on_delete=models.CASCADE,
        db_column="user_id",
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=None)
    height = models.IntegerField(default=None, verbose_name="키")
    weight = models.IntegerField(default=None, verbose_name="몸무게")
    stand = models.BooleanField(null=True, default=None, verbose_name="서서")
    sit = models.BooleanField(null=True, default=None, verbose_name="앉아서")
    balance = models.BooleanField(null=True, default=None, verbose_name="밸런스")
    core = models.BooleanField(null=True, default=None, verbose_name="코어")
    leg = models.BooleanField(null=True, default=None, verbose_name="다리")
    back = models.BooleanField(null=True, default=None, verbose_name="등")
    modified_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.user_id
