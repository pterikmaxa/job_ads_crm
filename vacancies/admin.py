from django.contrib import admin

from .models import JobPost


class ActiveCountryAdminMixin:
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "country":
            kwargs["queryset"] = db_field.remote_field.model.objects.filter(is_active=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(JobPost)
class JobPostAdmin(ActiveCountryAdminMixin, admin.ModelAdmin):
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
        "country__name",
        "country__code",
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
