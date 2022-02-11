from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.cores.models import TimeStampModel
from apps.users.models import User

# Create your models here.


class Exercise(models.Model):
    exercise_name = models.CharField(
        max_length=50, unique=True, verbose_name="exercise_name"
    )
    youtube_key = models.CharField(
        max_length=200, unique=True, verbose_name="youtube_key"
    )
    exercise_type = models.CharField(max_length=50, verbose_name="exercise_type")
    exercise_level = models.CharField(max_length=50, verbose_name="exercise_level")

    def __str__(self):
        return self.exercise_name


class Course(models.Model):
    course_name = models.CharField(
        max_length=50, unique=True, verbose_name="course_name"
    )
    exercises = models.ManyToManyField(
        Exercise, related_name="exercises", verbose_name="exercises"
    )
    avg_rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name="rating"
    )

    class Meta:
        ordering = ["avg_rating", "course_name"]

    def __str__(self):
        return self.course_name


class CourseReview(TimeStampModel):
    user_id = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="reviewer",
        verbose_name="user_id",
    )
    course_id = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="review_course",
        verbose_name="course_id",
    )
    content = models.TextField(max_length=300, verbose_name="content")
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name="rating"
    )
