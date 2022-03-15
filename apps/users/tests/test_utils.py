import pytest
from apps.users.models import User, UserDailyRecord, UserOption
from apps.users.utils import get_calories, get_decoded_token
from faker import Faker
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

fake = Faker()


@pytest.mark.django_db(transaction=True)
class TestUserUtils:
    @pytest.fixture
    def user(self):
        return User.objects.create_user(
            email=fake.email(), password=fake.password(length=8)
        )

    def test_get_calories_success(self):
        assert get_calories(weight=60, duration=3600)

    def test_get_calories_fail(self):
        with pytest.raises(TypeError):
            get_calories(duration=3600)

    def test_get_decoded_access_token_success(self, user):
        token = str(AccessToken.for_user(user))
        decoded_token = get_decoded_token(token)
        assert decoded_token["token_type"] == "access"

    def test_get_decoded_refresh_token_success(self, user):
        token = str(RefreshToken.for_user(user))
        decoded_token = get_decoded_token(token)
        assert decoded_token["token_type"] == "refresh"
