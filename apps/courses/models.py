from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.cores.models import DeleteModel, TimeStampModel
from apps.users.models import User


class Tag(models.Model):
    tag_name = models.CharField(max_length=30, verbose_name="해시태그")

    def __str__(self):
        return self.tag_name


class Exercise(models.Model):
    exercise_name = models.CharField(max_length=50, unique=True, verbose_name="운동 이름")
    youtube_key = models.CharField(
        max_length=200, unique=True, blank=True, verbose_name="유트브 키값"
    )
    youtube_start = models.PositiveSmallIntegerField(
        blank=True, verbose_name="유트브 시작 초"
    )
    youtube_end = models.PositiveSmallIntegerField(blank=True, verbose_name="유튜브 끝 초")
    exercise_type = models.CharField(max_length=50, verbose_name="운동 타입")
    description = models.CharField(max_length=200, blank=True, verbose_name="운동 설명")

    def __str__(self):
        return self.exercise_name


class Course(models.Model):
    course_name = models.CharField(max_length=50, unique=True, verbose_name="코스 이름")
    exercises = models.ManyToManyField(
        Exercise, related_name="course", verbose_name="구성 운동"
    )
    img_url = models.CharField(max_length=100, unique=True)
    avg_rating = models.FloatField(default=0, verbose_name="평균 평점")
    count_review = models.IntegerField(default=0, verbose_name="리뷰 개수")
    description = models.CharField(max_length=200, verbose_name="코스 설명", blank=True)
    hash_tag = models.ManyToManyField(
        Tag, related_name="course", verbose_name="해쉬태그", blank=True
    )
    review_user = models.ManyToManyField(
        User, related_name="review_course", verbose_name="유저 코스", through="CourseReview"
    )
    bookmark_user = models.ManyToManyField(
        User, related_name="bookmark_course", verbose_name="북마크 코스", through="BookMark"
    )
    stand_count = models.PositiveSmallIntegerField(default=0, verbose_name="서서 개수")
    sit_count = models.PositiveSmallIntegerField(default=0, verbose_name="앉아서 개수")
    balance_count = models.PositiveSmallIntegerField(default=0, verbose_name="밸런스 개수")
    core_count = models.PositiveSmallIntegerField(default=0, verbose_name="코어 개수")
    arm_count = models.PositiveSmallIntegerField(default=0, verbose_name="팔 개수")
    recline_count = models.PositiveSmallIntegerField(default=0, verbose_name="엎드려서 개수")

    class Meta:
        ordering = ["avg_rating", "course_name"]

    def __str__(self):
        return self.course_name


class CourseReview(TimeStampModel, DeleteModel):
    user_id = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="review",
        verbose_name="유저",
    )
    course_id = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="review",
        verbose_name="코스",
    )
    content = models.TextField(max_length=300, verbose_name="내용")
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name="평점"
    )

    def __str__(self):
        return f"{self.course_id} - {self.user_id.nickname}"


class BookMark(TimeStampModel):
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="bookmark",
        verbose_name="유저",
    )
    course_id = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="bookmark",
        verbose_name="코스",
    )

    def __str__(self):
        return f"{self.user_id.nickname} - {self.course_id}"
