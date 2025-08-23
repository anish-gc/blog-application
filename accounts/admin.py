from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account


@admin.register(Account)
class AccountAdmin(UserAdmin):
    # Fields shown in list view
    list_display = (
        "id",
        "username",
        "address",
        "is_active",
        "is_staff",
        "created_at",
        "updated_at",
    )
    list_filter = ("is_staff", "is_active", "created_at")
    search_fields = ("username", "address")
    ordering = ("-created_at",)

    # Fields that are read-only in admin
    readonly_fields = ("created_at", "updated_at", "last_login")

    # Field groups in the admin form
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal Info", {"fields": ("address",)}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Timestamps", {"fields": ("created_at", "updated_at", "last_login")}),
    )

    # Fields when creating a new user
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                ),
            },
        ),
    )
