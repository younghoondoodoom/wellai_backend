import csv
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.prod")
django.setup()

from apps.courses.models import Course, Exercise, Tag
from apps.users.models import User, UserDailyRecord, UserOption

EXERCISE_CSV_PATH = "./exercise.csv"

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


TAG_CSV_PATH = "./tag.csv"

with open(TAG_CSV_PATH, "r", encoding="utf-8") as tag:
    data_reader = csv.DictReader(tag)
    for row in data_reader:
        Tag.objects.create(tag_name=row["tag_name"])


COURSE_CSV_PATH = "./course.csv"

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

# Create User
import datetime
import random

from apps.users.utils import get_calories

test_user = User.objects.create_user(
    email="test@test.com", password="test123!", nickname="챠챠", is_staff=True
)
test_option = UserOption(
    user_id=test_user, gender="M", height=180, weight=70, is_stand=True, is_sit=True
)
test_option.save()

for i in range(1, 32):
    duration = random.randint(600, 1200)
    test_record = UserDailyRecord(
        user_id=test_user,
        exercise_date=datetime.date(2022, 1, i),
        exercise_duration=duration,
        calories_total=get_calories(70, duration),
    )
    test_record.save()

for i in range(1, 29):
    duration = random.randint(600, 1200)
    test_record = UserDailyRecord(
        user_id=test_user,
        exercise_date=datetime.date(2022, 2, i),
        exercise_duration=duration,
        calories_total=get_calories(70, duration),
    )
    test_record.save()

for i in range(1, 32):
    duration = random.randint(600, 1200)
    test_record = UserDailyRecord(
        user_id=test_user,
        exercise_date=datetime.date(2022, 3, i),
        exercise_duration=duration,
        calories_total=get_calories(70, duration),
    )
    test_record.save()

for i in range(1, 31):
    duration = random.randint(600, 1200)
    test_record = UserDailyRecord(
        user_id=test_user,
        exercise_date=datetime.date(2022, 4, i),
        exercise_duration=duration,
        calories_total=get_calories(70, duration),
    )
    test_record.save()

for i in range(1, 32):
    duration = random.randint(600, 1200)
    test_record = UserDailyRecord(
        user_id=test_user,
        exercise_date=datetime.date(2022, 5, i),
        exercise_duration=duration,
        calories_total=get_calories(70, duration),
    )
    test_record.save()

for i in range(1, 31):
    duration = random.randint(600, 1200)
    test_record = UserDailyRecord(
        user_id=test_user,
        exercise_date=datetime.date(2022, 6, i),
        exercise_duration=duration,
        calories_total=get_calories(70, duration),
    )
    test_record.save()

for i in range(1, 32):
    duration = random.randint(600, 1200)
    test_record = UserDailyRecord(
        user_id=test_user,
        exercise_date=datetime.date(2022, 7, i),
        exercise_duration=duration,
        calories_total=get_calories(70, duration),
    )
    test_record.save()

for i in range(1, 32):
    duration = random.randint(600, 1200)
    test_record = UserDailyRecord(
        user_id=test_user,
        exercise_date=datetime.date(2022, 8, i),
        exercise_duration=duration,
        calories_total=get_calories(70, duration),
    )
    test_record.save()

for i in range(1, 31):
    duration = random.randint(600, 1200)
    test_record = UserDailyRecord(
        user_id=test_user,
        exercise_date=datetime.date(2022, 9, i),
        exercise_duration=duration,
        calories_total=get_calories(70, duration),
    )
    test_record.save()

for i in range(1, 32):
    duration = random.randint(600, 1200)
    test_record = UserDailyRecord(
        user_id=test_user,
        exercise_date=datetime.date(2022, 10, i),
        exercise_duration=duration,
        calories_total=get_calories(70, duration),
    )
    test_record.save()

for i in range(1, 31):
    duration = random.randint(600, 1200)
    test_record = UserDailyRecord(
        user_id=test_user,
        exercise_date=datetime.date(2022, 11, i),
        exercise_duration=duration,
        calories_total=get_calories(70, duration),
    )
    test_record.save()

for i in range(1, 32):
    duration = random.randint(600, 1200)
    test_record = UserDailyRecord(
        user_id=test_user,
        exercise_date=datetime.date(2022, 12, i),
        exercise_duration=duration,
        calories_total=get_calories(70, duration),
    )
    test_record.save()
