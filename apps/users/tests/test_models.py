import factory
import pytest
from apps.users.models import User, UserInfo, UserOption
from django.urls import reverse
from pytest_factoryboy import register

from .factories import AdminUserFactory, UserFactory, UserInfoFactory, UserOptionFactory


@pytest.mark.django_db
def test_create_user_success():
    UserFactory.create()
    assert User.objects.count() == 1
