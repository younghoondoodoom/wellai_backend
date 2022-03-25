import json

import pytest
from apps.courses.models import *
from django.urls import reverse


@pytest.mark.django_db(transaction=True)
class TestCourse:
    @pytest.fixture
    def setup(self, client, django_user_model):
        password = "test123!"
        user = django_user_model.objects.create_user(
            email="test@test.com", password=password
        )
        user.set_password(password)

        # login
        url = reverse("login")
        res = client.post(
            url,
            json.dumps({"email": "test@test.com", "password": "test123!"}),
            content_type="application/json",
        )
        token = res.data["access"]

        # dumb data
        exercise = Exercise.objects.create(
            pk=1,
            exercise_name="test_exercise",
            youtube_key="test_key",
            youtube_start=0,
            youtube_end=60,
            exercise_type="서서",
        )
        tag = Tag.objects.create(pk=1, tag_name="test_tag")
        course = Course.objects.create(pk=1, course_name="test_course", img_url="test")
        course.exercises.add(exercise)
        course.hash_tag.add(tag)
        course.save()

        CourseReview.objects.create(
            pk=1, user_id=user, course_id=course, content="good test", rating=4
        )
        BookMark.objects.create(pk=1, user_id=user, course_id=course)

        return client, user, token, course, exercise

    def test_course_list_success(self, setup):
        client, user, token, course, exercise = setup
        url = reverse("course-list")
        http_author = f"Bearer {token}"
        res = client.get(
            url, {}, content_type="application/json", HTTP_AUTHORIZATION=http_author
        )
        assert res.status_code == 200
        assert res.data["results"][0]["course_name"] == "test_course"

    def test_exercise_detail_success(self, setup):
        client, user, token, course, exercise = setup
        url = reverse("exercise-detail", kwargs={"pk": 1})
        http_author = f"Bearer {token}"
        res = client.get(
            url, {}, content_type="application/json", HTTP_AUTHORIZATION=http_author
        )
        assert res.status_code == 200
        assert res.data["exercise_name"] == "test_exercise"

    def test_course_detail_success(self, setup):
        client, user, token, course, exercise = setup
        url = reverse("course-detail", kwargs={"pk": 1})
        http_author = f"Bearer {token}"
        res = client.get(
            url, {}, content_type="application/json", HTTP_AUTHORIZATION=http_author
        )
        assert res.status_code == 200
        assert res.data["course_name"] == course.course_name
        assert 1 in res.data["exercises"]
        assert res.data["hash_tag"][0]["tag_name"] == "test_tag"

    def test_course_detail_notfound_failure(self, setup):
        client, user, token, course, exercise = setup
        url = reverse("course-detail", kwargs={"pk": 300})
        http_author = f"Bearer {token}"
        res = client.get(
            url, {}, content_type="application/json", HTTP_AUTHORIZATION=http_author
        )
        assert res.status_code == 404
        assert res.data["message"] == "찾을 수 없습니다."

    def test_create_review_success(self, setup):
        client, user, token, course, exercise = setup
        course.delete()
        course.save()
        url = reverse("review-list-create", kwargs={"pk": 1})
        http_author = f"Bearer {token}"
        res = client.post(
            url,
            {"content": "create test", "rating": "5", "course_id": "1"},
            content_type="application/json",
            HTTP_AUTHORIZATION=http_author,
        )
        assert res.status_code == 201
        assert res.data["content"] == "create test"
        assert Course.objects.get(pk=1).avg_rating == 5.0

    def test_create_review_already_exist_failure(self, setup):
        client, user, token, course, exercise = setup
        url = reverse("review-list-create", kwargs={"pk": 1})
        http_author = f"Bearer {token}"
        res = client.post(
            url,
            {"content": "test", "rating": "5", "course_id": "1"},
            content_type="application/json",
            HTTP_AUTHORIZATION=http_author,
        )
        assert res.status_code == 400
        assert res.data["review"] == "이미 이 코스에 대한 리뷰가 있습니다!"

    def test_review_list_success(self, setup):
        client, user, token, course, exercise = setup
        url = reverse("review-list-create", kwargs={"pk": 1})
        http_author = f"Bearer {token}"
        res = client.get(
            url, {}, content_type="application/json", HTTP_AUTHORIZATION=http_author
        )
        assert res.status_code == 200
        assert res.data["results"][0]["content"] == "good test"

    def test_review_collection_success(self, setup):
        client, user, token, course, exercise = setup
        url = reverse("review-collection")
        http_author = f"Bearer {token}"
        res = client.get(
            url, {}, content_type="application/json", HTTP_AUTHORIZATION=http_author
        )
        assert res.status_code == 200
        assert res.data[0]["content"] == "good test"

    def test_retrieve_myreview_success(self, setup):
        client, user, token, course, exercise = setup
        url = reverse("myreview-retrieve", kwargs={"pk": 1})
        http_author = f"Bearer {token}"
        res = client.get(
            url, {}, content_type="application/json", HTTP_AUTHORIZATION=http_author
        )
        assert res.status_code == 200
        assert res.data[0]["content"] == "good test"

    def test_delete_review_success(self, setup):
        client, user, token, course, exercise = setup
        url = reverse("review-update-delete", kwargs={"pk": 1})
        http_author = f"Bearer {token}"
        res = client.delete(
            url, {}, content_type="application/json", HTTP_AUTHORIZATION=http_author
        )
        assert res.status_code == 204
        assert user.review.exists() == False

    def test_update_review_success(self, setup):
        client, user, token, course, exercise = setup
        url = reverse("review-update-delete", kwargs={"pk": 1})
        http_author = f"Bearer {token}"
        res = client.put(
            url,
            {"content": "update test", "rating": 1},
            content_type="application/json",
            HTTP_AUTHORIZATION=http_author,
        )
        assert res.status_code == 200
        assert Course.objects.get(pk=1).avg_rating == 1

    def test_bookmark_list_success(self, setup):
        client, user, token, course, exercise = setup
        url = reverse("course-bookmark")
        http_author = f"Bearer {token}"
        res = client.get(
            url,
            {},
            content_type="application/json",
            HTTP_AUTHORIZATION=http_author,
        )
        assert res.status_code == 200
        assert user.bookmark.first().course_id == course

    def test_create_bookmark_success(self, setup):
        client, user, token, course, exercise = setup
        bookmark = BookMark.objects.get(pk=1)
        bookmark.delete()
        url = reverse("course-bookmark")
        http_author = f"Bearer {token}"
        res = client.post(
            url,
            {"course_id": 1},
            content_type="application/json",
            HTTP_AUTHORIZATION=http_author,
        )
        assert res.status_code == 201
        assert res.data["course_id"] == course.id

    def test_create_bookmark_already_exists_failure(self, setup):
        client, user, token, course, exercise = setup
        url = reverse("course-bookmark")
        http_author = f"Bearer {token}"
        res = client.post(
            url,
            {"course_id": 1},
            content_type="application/json",
            HTTP_AUTHORIZATION=http_author,
        )
        assert res.status_code == 400
        assert res.data["bookmark"] == "이미 이 코스를 북마크 하셨습니다!"

    def test_delete_bookmark_success(self, setup):
        client, user, token, course, exercise = setup
        url = reverse("course-bookmark-delete", kwargs={"pk": 1})
        http_author = f"Bearer {token}"
        res = client.delete(
            url, {}, content_type="application/json", HTTP_AUTHORIZATION=http_author
        )
        assert res.status_code == 204
        assert user.bookmark.exists() == False
