import uuid

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import EmailValidator, RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .validators import NicknameValidator, PasswordValidator


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

    user_id = models.EmailField(unique=True, verbose_name="이메일")

    nickname = models.CharField(
        unique=True,
        max_length=64,
        validators=[NicknameValidator()],
        verbose_name="닉네임",
    )
    password = models.CharField(
        _("password"),
        max_length=128,
        validators=[PasswordValidator()],
    )
    uid = models.UUIDField(
        unique=True,
        editable=False,
        default=uuid.uuid4,
        verbose_name="외부공개키",
    )
    date_joined = models.DateTimeField(
        default=timezone.now, editable=False, verbose_name="가입날짜"
    )
    is_deleted = models.BooleanField(default=False, verbose_name="계정삭제여부")
    is_staff = models.BooleanField(default=False, verbose_name="관리자여부")

    USERNAME_FIELD = "user_id"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.user_id


class UserDailyInfo(models.Model):
    today = timezone.now()

    user_id = models.ForeignKey(
        User,
        related_name="daily_info",
        on_delete=models.CASCADE,
        db_column="user_id",
    )
    exercise_date = models.CharField(
        default=today.strftime("%Y-%m-%d"),
        max_length=15,
        verbose_name="운동날짜",
    )
    exercise_total = models.PositiveSmallIntegerField(
        default=0, verbose_name="일별 총 운동시간"
    )
    calories_total = models.PositiveSmallIntegerField(
        default=0, verbose_name="일별 총 소모칼로리"
    )
    # 일~토 : 0~6
    exercise_day = models.PositiveSmallIntegerField(
        default=int(today.strftime("%w")), editable=False, verbose_name="요일"
    )
    modified_at = models.DateTimeField(
        auto_now=True, editable=False, verbose_name="최근수정날짜"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user_id", "exercise_date"], name="users_userdailyinfo_history"
            )
        ]

    def __str__(self):
        return f"{self.user_id}: {self.exercise_total}mins, {self.calories_total}cals"


class UserOption(models.Model):
    GENDER_CHOICES = [
        (None, ""),
        ("F", "여"),
        ("M", "남"),
    ]
    user_id = models.OneToOneField(
        User,
        related_name="option",
        on_delete=models.CASCADE,
        db_column="user_id",
    )
    gender = models.CharField(
        blank=True,
        null=True,
        max_length=1,
        choices=GENDER_CHOICES,
        default=None,
        verbose_name="성별",
    )
    height = models.PositiveSmallIntegerField(default=0, verbose_name="키")
    weight = models.PositiveSmallIntegerField(default=0, verbose_name="몸무게")
    stand = models.BooleanField(default=False, verbose_name="서서")
    sit = models.BooleanField(default=False, verbose_name="앉아서")
    balance = models.BooleanField(default=False, verbose_name="밸런스")
    core = models.BooleanField(default=False, verbose_name="코어")
    leg = models.BooleanField(default=False, verbose_name="다리")
    back = models.BooleanField(default=False, verbose_name="등")
    modified_at = models.DateTimeField(
        auto_now=True, editable=False, verbose_name="최근수정날짜"
    )

    def __str__(self):
        return f"{self.user_id}"
