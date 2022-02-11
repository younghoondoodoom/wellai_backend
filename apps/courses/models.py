from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# Create your models here.


class Exercise(models.Model):
    exercise_name = models.CharField(
        max_length=50, unique=True, verbose_name="exercise_name"
    )
    youtube_key = models.CharField(
        max_length=200, unique=True, verbose_name="youtube_key"
    )
    exercise_type = models.CharField(max_length=50, verbose_name="exercise_type")

    def __str__(self):
        return self.exercise_name


class Course(models.Model):
    course_name = models.CharField(
        max_length=50, unique=True, verbose_name="course_name"
    )
    exercises = models.ManyToManyField(
        Exercise, related_name="exercises", verbose_name="exercises"
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name="rating"
    )

    class Meta:
        ordering = ["rating", "course_name"]

    def __str__(self):
        return self.course_name
