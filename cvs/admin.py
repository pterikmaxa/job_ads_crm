from django.contrib import admin

from .models import CVProfile


class ActiveCountryAdminMixin:
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "country":
            kwargs["queryset"] = db_field.remote_field.model.objects.filter(is_active=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(CVProfile)
class CVProfileAdmin(ActiveCountryAdminMixin, admin.ModelAdmin):
    list_display = (
        "title",
        "country",
        "specialization",
        "is_active",
        "created_at",
        "updated_at",
    )
    search_fields = ("title", "country__name", "country__code", "specialization", "short_description")
    list_filter = ("is_active", "country", "specialization")
