from django import forms
from django.contrib import admin
from django.db import OperationalError, ProgrammingError

from sources.models import SearchTechnology

from .models import CVProfile


class CVProfileAdminForm(forms.ModelForm):
    technology_choice = forms.ChoiceField(
        label="Выбрать технологию",
        required=False,
        choices=[("", "---------")],
    )

    class Meta:
        model = CVProfile
        fields = "__all__"
        labels = {
            "title": "Название",
            "country": "Страна",
            "specialization": "Специализация",
            "short_description": "Краткое описание",
            "file_path": "Путь к файлу",
            "is_active": "Активен",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            technologies = SearchTechnology.objects.filter(is_active=True).order_by("sort_order")
            self.fields["technology_choice"].choices = [
                ("", "---------"),
                *[(t.name, t.name) for t in technologies],
            ]
        except (OperationalError, ProgrammingError):
            self.fields["technology_choice"].choices = [("", "---------")]


@admin.register(CVProfile)
class CVProfileAdmin(admin.ModelAdmin):
    form = CVProfileAdminForm

    fieldsets = (
        (None, {
            "fields": (
                "title",
                "country",
                "specialization",
                "technology_choice",
                "short_description",
                "file_path",
                "is_active",
            )
        }),
    )

    list_display = (
        "title",
        "country",
        "specialization",
        "is_active",
        "created_at",
    )
    search_fields = (
        "title",
        "country__name",
        "country__code",
        "specialization",
        "short_description",
        "file_path",
    )
    list_filter = (
        "is_active",
        "country",
    )

    class Media:
        css = {
            "all": ("admin/cvprofile_admin.css",)
        }
        js = ("admin/cvprofile_admin.js",)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "country":
            kwargs["queryset"] = db_field.remote_field.model.objects.filter(is_active=True)

        field = super().formfield_for_foreignkey(db_field, request, **kwargs)

        if db_field.name == "country":
            widget = field.widget
            if hasattr(widget, "can_add_related"):
                widget.can_add_related = False
            if hasattr(widget, "can_change_related"):
                widget.can_change_related = False
            if hasattr(widget, "can_delete_related"):
                widget.can_delete_related = False
            if hasattr(widget, "can_view_related"):
                widget.can_view_related = False

        return field
