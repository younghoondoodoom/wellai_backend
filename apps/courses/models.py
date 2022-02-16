from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.cores.models import DeleteModel, TimeStampModel
from apps.users.models import User

# Create your models here.


class Tag(models.Model):
    tag = models.CharField(max_length=30, verbose_name="해시태그")

    def __str__(self):
        return self.tag


class Exercise(models.Model):
    exercise_name = models.CharField(max_length=50, unique=True, verbose_name="운동 이름")
    youtube_key = models.CharField(max_length=200, unique=True, verbose_name="유트브 키값")
    exercise_type = models.CharField(max_length=50, verbose_name="운동 타입")
    exercise_level = models.CharField(max_length=50, verbose_name="운동 레벨")

    def __str__(self):
        return self.exercise_name


class Course(models.Model):
    course_name = models.CharField(max_length=50, unique=True, verbose_name="코스 이름")
    exercises = models.ManyToManyField(
        Exercise, related_name="exercises", verbose_name="구성 운동"
    )
    avg_rating = models.FloatField(default=0, verbose_name="평균 평점")
    count_review = models.IntegerField(default=0, verbose_name="리뷰 개수")
    hash_tag = models.ManyToManyField(Tag, related_name="hash_tag", verbose_name="해쉬태그")

    class Meta:
        ordering = ["avg_rating", "course_name"]

    def __str__(self):
        return self.course_name


class CourseReview(TimeStampModel, DeleteModel):
    user_id = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="reviewer",
        verbose_name="유저",
    )
    course_id = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="review_course",
        verbose_name="코스",
    )
    content = models.TextField(max_length=300, verbose_name="내용")
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name="평점"
    )

    def __str__(self):
        return str(self.course_id) + " - " + str(self.user_id)
