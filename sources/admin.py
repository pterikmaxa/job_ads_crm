from django.contrib import admin
from django.db.models import Case, IntegerField, Value, When
from django.utils.html import format_html

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
    exclude = ("color_status",)
    list_display = (
        "status_indicator",
        "name",
        "url",
        "country",
        "priority",
        "daily_plan",
        "processed_today",
        "is_active",
    )
    search_fields = ("name", "country__name", "country__code", "url", "comment")
    list_filter = ("is_active", "country", "priority", "color_status")

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ()
        return ("status_indicator",)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(
            _status_order=Case(
                When(color_status=JobSite.Status.PROBLEM, then=Value(1)),
                When(color_status=JobSite.Status.ATTENTION, then=Value(2)),
                When(color_status=JobSite.Status.OK, then=Value(3)),
                When(color_status=JobSite.Status.INACTIVE, then=Value(4)),
                When(color_status=JobSite.Status.BROKEN, then=Value(5)),
                default=Value(6),
                output_field=IntegerField(),
            )
        )

    @admin.display(ordering="_status_order", description="Status")
    def status_indicator(self, obj):
        colors = {
            JobSite.Status.PROBLEM: "#dc2626",
            JobSite.Status.ATTENTION: "#facc15",
            JobSite.Status.OK: "#16a34a",
            JobSite.Status.INACTIVE: "#9ca3af",
            JobSite.Status.BROKEN: "#2563eb",
        }
        labels = dict(JobSite.Status.choices)
        color = colors.get(obj.color_status, "#9ca3af")
        label = labels.get(obj.color_status, obj.color_status)
        return format_html(
            '<span title="{}" style="display:inline-block;width:14px;height:14px;'
            'border-radius:3px;background:{};vertical-align:middle;"></span> '
            '<span>{}</span>',
            label,
            color,
            label,
        )


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
