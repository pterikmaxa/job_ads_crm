from django.contrib import admin

from .models import CVProfile


@admin.register(CVProfile)
class CVProfileAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "country",
        "specialization",
        "is_active",
        "created_at",
        "updated_at",
    )
    search_fields = ("title", "country", "specialization", "short_description")
    list_filter = ("is_active", "country", "specialization")
