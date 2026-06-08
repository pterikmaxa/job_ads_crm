from django.contrib import admin

from .models import JobPost


@admin.register(JobPost)
class JobPostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "company",
        "job_site",
        "cv_profile",
        "country",
        "city",
        "status",
        "response_received",
        "added_at",
    )
    search_fields = (
        "title",
        "company",
        "country",
        "city",
        "url",
        "source_name",
        "provider_name",
        "job_site__name",
        "cv_profile__title",
    )
    list_filter = (
        "status",
        "response_received",
        "country",
        "job_site",
        "cv_profile",
    )
