from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import User


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
        (_("Status"), {"fields": ("is_deleted",)}),
    )
    search_fields = ["user_id"]
    list_filter = ["last_login", "is_deleted"]
    ordering = ["created_at"]


admin.site.register(User, MyUserAdmin)
