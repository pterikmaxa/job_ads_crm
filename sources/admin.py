from django.contrib import admin

from .models import JobSite, SearchSignature


@admin.register(JobSite)
class JobSiteAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "country",
        "priority",
        "daily_plan",
        "processed_today",
        "color_status",
        "is_active",
    )
    search_fields = ("name", "country", "url", "comment")
    list_filter = ("is_active", "country", "priority", "color_status")


@admin.register(SearchSignature)
class SearchSignatureAdmin(admin.ModelAdmin):
    list_display = (
        "search_text",
        "job_site",
        "country",
        "technology",
        "is_active",
        "created_at",
    )
    search_fields = ("search_text", "country", "technology", "job_site__name")
    list_filter = ("is_active", "country", "technology", "job_site")
