import pytest
from apps.users.models import User, UserDailyRecord, UserOption
from django.utils import timezone
from faker import Faker

fake = Faker()


@pytest.mark.django_db(transaction=True)
class TestUserModel:
    @pytest.fixture()
    def setup_user(self):
        user = User.objects.create_user(
            email=fake.email(),
            password=fake.password(length=8),
        )
        return user

    def test_create_user_success(self, setup_user):
        user = setup_user
        assert str(user) == user.email

    def test_create_user_email_empty_fail(self):
        with pytest.raises(ValueError):
            User.objects.create_user(email="", password=fake.password(length=8))

    def test_create_user_password_empty_fail(self):
        with pytest.raises(ValueError):
            User.objects.create_user(email=fake.email(), password="")

    def test_create_superuser_success(self):
        User.objects.create_superuser(email=fake.email(), password="1234")

    def test_create_superuser_email_empty_fail(self):
        with pytest.raises(ValueError):
            User.objects.create_superuser(email="", password="1234")

    def test_create_superuser_is_staff_fail(self):
        with pytest.raises(ValueError):
            User.objects.create_superuser(
                email=fake.email(), password="1234", is_staff=False
            )

    def test_create_useroption_success(self, setup_user):
        user = setup_user
        option = UserOption.objects.create(
            user_id=user,
            gender="F",
            height=0,
            weight=0,
            is_stand=False,
            is_sit=False,
            is_balance=True,
            is_core=False,
            is_arm=True,
            is_recline=False,
        )
        assert str(option) == option.user_id.email

    def test_create_user_daily_record_success(self, setup_user):
        user = setup_user
        date = timezone.now()
        record = UserDailyRecord.objects.create(
            user_id=user, exercise_date=date, exercise_duration=3600
        )
        assert str(record) == f"{user.email} - {date}"
