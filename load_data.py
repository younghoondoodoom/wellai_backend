import csv
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.prod")
django.setup()

from apps.courses.models import Course, Exercise

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
            description=row["설명"],
        )
