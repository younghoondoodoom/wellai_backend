from collections import OrderedDict

import factory
from faker import Faker
from pytest_factoryboy import register

# faker 랜덤 데이터 생성시 언어 선택 기준
locale_odict = OrderedDict(
    [
        ("en-US", 1),
        ("ko-KR", 2),
    ]
)
fake = Faker(locale_odict)


class UserFactory(factory.django.DjangoModelFactory):

    user_id = fake.email()
    nickname = fake.name()
    password = fake.password(length=8)  # !@#$%^&*()_+

    class Meta:
        model = "users.User"


class AdminUserFactory(UserFactory):
    is_staff = True
    is_superuser = True


class UserInfoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "users.UserInfo"
        # django_get_or_create = ("user_id",)

    user_id = factory.SubFactory(UserFactory)
    # 1일 = 1440분
    exercise_total = fake.random_element(
        elements=(None, fake.random_int(min=0, max=1440))
    )
    calories_total = fake.random_element(elements=(None, fake.random_number()))


class UserOptionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "users.UserOption"
        # django_get_or_create = ("user_id",)

    user_id = factory.SubFactory(UserFactory)
    gender = fake.random_element(elements=(None, "F", "M"))
    height = fake.random_element(elements=(None, fake.random_int(min=0, max=500)))
    weight = fake.random_element(elements=(None, fake.random_int(min=0, max=1500)))
    stand = fake.random_element(elements=(None, True))
    sit = fake.random_element(elements=(None, True))
    balance = fake.random_element(elements=(None, True))
    core = fake.random_element(elements=(None, True))
    leg = fake.random_element(elements=(None, True))
    back = fake.random_element(elements=(None, True))


register(UserFactory)
register(UserInfoFactory)
register(UserOptionFactory)
