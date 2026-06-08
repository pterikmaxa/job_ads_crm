from django.contrib import admin

from .models import Country, JobSite, SearchSignature


class ActiveCountryAdminMixin:
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "country":
            kwargs["queryset"] = Country.objects.filter(is_active=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "is_active", "created_at", "updated_at")
    search_fields = ("name", "code")
    list_filter = ("is_active",)


@admin.register(JobSite)
class JobSiteAdmin(ActiveCountryAdminMixin, admin.ModelAdmin):
    list_display = (
        "name",
        "country",
        "priority",
        "daily_plan",
        "processed_today",
        "color_status",
        "is_active",
    )
    search_fields = ("name", "country__name", "country__code", "url", "comment")
    list_filter = ("is_active", "country", "priority", "color_status")


@admin.register(SearchSignature)
class SearchSignatureAdmin(ActiveCountryAdminMixin, admin.ModelAdmin):
    list_display = (
        "search_text",
        "job_site",
        "country",
        "technology",
        "is_active",
        "created_at",
    )
    search_fields = ("search_text", "country__name", "country__code", "technology", "job_site__name")
    list_filter = ("is_active", "country", "technology", "job_site")
