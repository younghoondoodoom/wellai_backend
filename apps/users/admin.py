# Register your models here.
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import User, UserInfo, UserOption


# Register your models here.
class MyUserAdmin(admin.ModelAdmin):
    model = User
    list_display = [
        "user_id",
        "nickname",
        "last_login",
        "uid",
        "is_active",
        "is_deleted",
        "is_staff",
    ]

    fieldsets = (
        (
            _("Personal info"),
            {
                "fields": (
                    "user_id",
                    "nickname",
                    "password",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
        (_("Status"), {"fields": ("is_deleted", "is_staff")}),
    )
    search_fields = ["user_id"]
    list_filter = ["last_login", "is_deleted", "is_staff"]
    ordering = ["date_joined"]


class MyUserInfoAdmin(admin.ModelAdmin):
    model = UserInfo
    list_display = [
        "user_id",
        "exercise_total",
        "calories_total",
        "exercise_date",
        "exercise_day",
        "modified_at",
    ]

    fields = (
        "user_id",
        "exercise_total",
        "calories_total",
        "exercise_date",
        "exercise_day",
    )
    search_fields = ["user_id"]
    list_filter = ["exercise_date", "exercise_day"]
    ordering = ["user_id"]


class MyUserOptionAdmin(admin.ModelAdmin):
    model = UserOption
    list_display = [
        "user_id",
        "gender",
        "height",
        "weight",
        "stand",
        "sit",
        "balance",
        "core",
        "leg",
        "back",
        "modified_at",
    ]
    fieldsets = (
        (
            _("Personal info"),
            {
                "fields": (
                    "user_id",
                    "gender",
                    "height",
                    "weight",
                )
            },
        ),
        (
            _("favorite exercise"),
            {"fields": ("stand", "sit", "balance", "core", "leg", "back")},
        ),
    )

    search_fields = ["user_id"]
    list_filter = ["gender"]
    ordering = ["user_id"]


admin.site.register(User, MyUserAdmin)
admin.site.register(UserInfo, MyUserInfoAdmin)
admin.site.register(UserOption, MyUserOptionAdmin)
