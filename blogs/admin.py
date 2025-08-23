from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "author",
        "created_at",
        "updated_at",
        "is_active",
    )
    list_filter = ("is_active", "created_at", "updated_at", "author")
    search_fields = ("title", "content", "author__username")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")  # prevent manual edits
    fieldsets = (
        (None, {"fields": ("title", "content", "author", "is_active", "remarks")}),
        (
            "Timestamps",
            {
                "fields": ("created_at", "updated_at"),
            },
        ),
    )
