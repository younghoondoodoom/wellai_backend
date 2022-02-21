import pytest
from apps.courses.models import Exercise

from fixtures import exercise_one


@pytest.mark.django_db
def test_create_exercise_one(exercise_one):
    assert exercise_one.exercise_name == "물구나무 서기"
    assert exercise_one.youtube_key == "LWq35rPAiYc"
