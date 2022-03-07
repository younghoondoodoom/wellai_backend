import csv
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.prod")
django.setup()

from apps.courses.models import Course, Exercise, Tag

EXERCISE_CSV_PATH = "data/exercise.csv"

with open(EXERCISE_CSV_PATH, "r", encoding="utf-8") as exercises:
    data_reader = csv.DictReader(exercises)
    for row in data_reader:
        Exercise.objects.create(
            pk=row["pk"],
            exercise_name=row["한국어 자세이름"],
            youtube_key=row["유튜브 키"],
            youtube_start=row["시작시간(좌측유튭영상)"],
            youtube_end=row["끝나는시간(좌측유튭영상)"],
            exercise_type=row["6분류"],
        )


TAG_CSV_PATH = "data/tag.csv"

with open(TAG_CSV_PATH, "r", encoding="utf-8") as tag:
    data_reader = csv.DictReader(tag)
    for row in data_reader:
        Tag.objects.create(tag_name=row["tag_name"])


COURSE_CSV_PATH = "data/course.csv"

with open(COURSE_CSV_PATH, "r", encoding="utf-8") as course:
    data_reader = csv.DictReader(course)
    for row in data_reader:
        data = Course(
            course_name=row["course_name"],
            img_url=row["img_url"],
            description=row["description"],
            stand_count=row["stand_count"],
            sit_count=row["sit_count"],
            balance_count=row["balance_count"],
            core_count=row["core_count"],
            arm_count=row["arm_count"],
            recline_count=row["recline_count"],
        )
        data.save()
        exercises = row["exercises"].strip().split(" ")
        hash_tag = row["hash_tag"].strip().split(" ")
        for i in range(len(exercises)):
            exercise = Exercise.objects.get(pk=exercises[i])
            data.exercises.add(exercise)
        for i in range(len(hash_tag)):
            tag = Tag.objects.get(tag_name=hash_tag[i])
            data.hash_tag.add(tag)
        data.save()
