from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Exercise(models.Model):
    exercise_name = models.CharField(max_length=50, unique=True, verbose_name="운동이름")
    youtube_key = models.CharField(max_length=200, unique=True, verbose_name="운동영상")
    exercise_type = models.CharField(max_length=50, verbose_name="운동타입")
    
    def __str__(self):
        return self.exercise_name
    

class Course(models.Model):
    course_name = models.CharField(max_length=50, unique=True, verbose_name="코스이름")
    exercises = models.ManyToManyField(Exercise, related_name="exercises", verbose_name="코스평점")
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name="평점")

    class Meta:
        ordering = ["rating", "course_name"]
    
    def __str__(self):
        return self.course_name