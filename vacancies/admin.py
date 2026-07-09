from django import forms
from django.contrib import admin
from django.db import OperationalError, ProgrammingError

from .models import (
    Company,
    JobPost,
    JobPostStatus,
    Lead,
    LeadAction,
    LeadResponse,
)


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


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "website",
        "updated_at",
    )
    search_fields = (
        "name",
        "website",
        "comment",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )


class LeadActionInline(admin.TabularInline):
    model = LeadAction
    extra = 0
    fields = (
        "action_type",
        "status",
        "planned_date",
        "action_date",
        "contact_value",
        "cv_text",
        "comment",
    )
    show_change_link = True


class LeadResponseInline(admin.TabularInline):
    model = LeadResponse
    extra = 0
    fields = (
        "response_type",
        "response_channel",
        "response_date",
        "from_value",
        "next_action_date",
        "comment",
    )
    show_change_link = True


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "company",
        "language",
        "location_text",
        "priority",
        "status",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "title",
        "company__name",
        "url",
        "description_text",
        "technology_text",
        "comment",
    )
    list_filter = (
        "status",
        "priority",
        "language",
        "technologies",
        "company",
    )
    filter_horizontal = (
        "technologies",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    fieldsets = (
        (
            "Основное",
            {
                "fields": (
                    "title",
                    "company",
                    "url",
                    "language",
                    "location_text",
                    "priority",
                    "status",
                )
            },
        ),
        (
            "Описание",
            {
                "fields": (
                    "description_text",
                    "comment",
                )
            },
        ),
        (
            "Технологии",
            {
                "fields": (
                    "technologies",
                    "technology_text",
                )
            },
        ),
        (
            "Служебные даты",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )
    inlines = (
        LeadActionInline,
        LeadResponseInline,
    )


@admin.register(LeadAction)
class LeadActionAdmin(admin.ModelAdmin):
    list_display = (
        "lead",
        "action_type",
        "status",
        "planned_date",
        "action_date",
        "contact_value",
        "cv_text",
        "updated_at",
    )
    search_fields = (
        "lead__title",
        "lead__company__name",
        "contact_value",
        "cv_text",
        "message_text",
        "comment",
    )
    list_filter = (
        "action_type",
        "status",
        "planned_date",
        "action_date",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(LeadResponse)
class LeadResponseAdmin(admin.ModelAdmin):
    list_display = (
        "lead",
        "response_type",
        "response_channel",
        "response_date",
        "from_value",
        "next_action_date",
        "updated_at",
    )
    search_fields = (
        "lead__title",
        "lead__company__name",
        "from_value",
        "response_text",
        "next_action",
        "comment",
    )
    list_filter = (
        "response_type",
        "response_channel",
        "response_date",
        "next_action_date",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
