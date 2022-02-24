from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Team10",
        default_version="v1",
        description="인공지능 웹서비스 프로젝트",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


extra_patterns = [
    path("admin/", admin.site.urls),
    path("users/", include("apps.users.urls")),
    path("course/", include("apps.courses.urls")),
]

docs_patterns = [
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
]

urlpatterns = [
    path("api/", include(extra_patterns)),
    path("docs/", include(docs_patterns)),
]
