import pytest
from apps.courses.models import Exercise


@pytest.fixture
def exercise_one(db):
    return Exercise.objects.create(
        exercise_name="물구나무 서기",
        youtube_key="LWq35rPAiYc",
        exercise_type="standing",
        exercise_level="high",
    )
