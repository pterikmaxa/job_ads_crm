from django import forms
from django.contrib import admin
from django.db import OperationalError, ProgrammingError

from .models import JobPost, JobPostStatus


class CleanRelatedWidgetMixin:
    related_fields_without_buttons = {"country", "job_site"}

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "country":
            kwargs["queryset"] = db_field.remote_field.model.objects.filter(is_active=True)

        field = super().formfield_for_foreignkey(db_field, request, **kwargs)

        if db_field.name in self.related_fields_without_buttons:
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


class JobPostAdminForm(forms.ModelForm):
    status = forms.ChoiceField(label="Статус", required=True)

    class Meta:
        model = JobPost
        fields = "__all__"
        labels = {
            "job_site": "Сайт вакансий",
            "cv_profile": "Профиль резюме",
            "url": "Ссылка",
            "title": "Название вакансии",
            "company": "Компания",
            "country": "Страна",
            "city": "Город",
            "source_name": "Название источника",
            "provider_name": "Провайдер / агентство",
            "applied_at": "Дата отклика",
            "response_received": "Ответ получен",
            "comment": "Комментарий",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            statuses = JobPostStatus.objects.filter(is_active=True).order_by("sort_order")
            self.fields["status"].choices = [(s.code, s.name) for s in statuses]
        except (OperationalError, ProgrammingError):
            self.fields["status"].choices = []

        current_status = self.initial.get("status") or getattr(self.instance, "status", None)
        if current_status and current_status not in dict(self.fields["status"].choices):
            self.fields["status"].choices = [
                (current_status, current_status),
                *self.fields["status"].choices,
            ]


@admin.register(JobPost)
class JobPostAdmin(CleanRelatedWidgetMixin, admin.ModelAdmin):
    form = JobPostAdminForm

    list_display = (
        "title",
        "company",
        "job_site",
        "cv_profile",
        "country",
        "city",
        "status_label",
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

    class Media:
        js = ("admin/jobpost_admin.js",)

    @admin.display(description="Статус", ordering="status")
    def status_label(self, obj):
        return obj.status_name
