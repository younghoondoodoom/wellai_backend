from collections import OrderedDict

import factory
from apps.users.tests.factories import UserFactory
from faker import Faker
from pytest_factoryboy import register

locale_odict = OrderedDict(
    [
        ("en-US", 2),
        ("ko-KR", 1),
    ]
)
fake = Faker(locale_odict)


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "courses.Tag"

    tag_name = fake.name()


class ExerciseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "courses.Exercise"

    exercise_name = fake.name()
    youtube_key = fake.password(length=200)
    youtube_start = fake.random_int(min=0, max=100)
    youtube_end = fake.random_int(min=100, max=200)
    exercise_type = fake.name()


class CourseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "courses.Course"

    course_name = fake.name()
    exercises = factory.SubFactory(ExerciseFactory)
    img_url = fake.image_url()
    avg_rating = fake.pyfloat(left_digits=1, right_digits=1, min_value=0, max_value=5)
    count_review = fake.random_int()
    description = fake.paragraph(nb_sentences=3, variable_nb_sentences=False)
    hash_tag = factory.SubFactory(TagFactory)
    stand_count = fake.random_int(min=0, max=5)
    sit_count = fake.random_int(min=0, max=5)
    balance_count = fake.random_int(min=0, max=5)
    core_count = fake.random_int(min=0, max=5)
    arm_count = fake.random_int(min=0, max=5)
    recline_count = fake.random_int(min=0, max=5)


class CourseReviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "courses.CourseReview"

    user_id = factory.SubFactory(UserFactory)
    course_id = factory.SubFactory(CourseFactory)
    content = fake.paragraph(nb_sentences=8, variable_nb_sentences=False)
    rating = fake.random_int(min=0, max=5)


class BookMarkFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "courses.BookMark"

    user_id = factory.SubFactory(UserFactory)
    course_id = factory.SubFactory(CourseFactory)


register(ExerciseFactory)
register(CourseFactory)
register(CourseReviewFactory)
register(BookMarkFactory)
