from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import User, UserDailyRecord, UserOption


class UserRecordInline(admin.TabularInline):
    model = UserDailyRecord


class UserOptionInline(admin.TabularInline):
    model = UserOption


class MyUserRecordAdmin(admin.ModelAdmin):
    model = UserDailyRecord

    list_display = [
        "user_id",
        "exercise_duration",
        "calories_total",
        "exercise_date",
        "exercise_day",
        "modified_at",
    ]

    fields = (
        "user_id",
        "exercise_duration",
        "calories_total",
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
        "is_stand",
        "is_sit",
        "is_balance",
        "is_core",
        "is_leg",
        "is_back",
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
            {
                "fields": (
                    "is_stand",
                    "is_sit",
                    "is_balance",
                    "is_core",
                    "is_leg",
                    "is_back",
                )
            },
        ),
    )

    search_fields = ["user_id"]
    list_filter = ["gender"]
    ordering = ["user_id"]


class MyUserAdmin(admin.ModelAdmin):
    model = User

    list_display = [
        "email",
        "nickname",
        "last_login",
        "is_active",
        "is_deleted",
        "is_staff",
    ]

    fieldsets = (
        (
            _("Personal info"),
            {
                "fields": (
                    "email",
                    "nickname",
                    "password",
                )
            },
        ),
        (_("Status"), {"fields": ("is_deleted", "is_staff")}),
    )
    inlines = [UserRecordInline, UserOptionInline]
    search_fields = ["email"]
    list_filter = ["last_login", "is_deleted", "is_staff"]
    ordering = ["created_at"]


admin.site.register(User, MyUserAdmin)
admin.site.register(UserDailyRecord, MyUserRecordAdmin)
admin.site.register(UserOption, MyUserOptionAdmin)
