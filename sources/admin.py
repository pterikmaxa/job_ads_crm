from django import forms
from django.contrib import admin
from django.db import OperationalError, ProgrammingError
from django.db.models import Case, IntegerField, Value, When
from django.utils.html import format_html

from .models import Country, JobSite, SearchSignature, SearchTechnology


class CleanRelatedWidgetMixin:
    related_fields_without_buttons = {"country", "job_site"}

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "country":
            kwargs["queryset"] = Country.objects.filter(is_active=True)

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


class JobSiteAdminForm(forms.ModelForm):
    class Meta:
        model = JobSite
        fields = "__all__"
        labels = {
            "name": "Название",
            "country": "Страна",
            "url": "Сайт",
            "priority": "Приоритет",
            "daily_plan": "План в день",
            "processed_today": "Обработано сегодня",
            "comment": "Комментарий",
            "is_active": "Активен",
        }
        widgets = {
            "priority": forms.NumberInput(attrs={"class": "vIntegerField spin-field", "min": 0}),
            "daily_plan": forms.NumberInput(attrs={"class": "vIntegerField spin-field", "min": 0}),
            "processed_today": forms.NumberInput(attrs={"class": "vIntegerField spin-field", "min": 0}),
        }


class SearchSignatureAdminForm(forms.ModelForm):
    technology_choice = forms.ChoiceField(
        label="Выбрать технологию",
        required=False,
        choices=[("", "---------")],
    )

    class Meta:
        model = SearchSignature
        fields = "__all__"
        labels = {
            "job_site": "Сайт вакансий",
            "search_text": "Поисковый запрос",
            "country": "Страна",
            "technology": "Технология",
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


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "is_active", "created_at", "updated_at")
    search_fields = ("name", "code")
    list_filter = ("is_active",)


@admin.register(JobSite)
class JobSiteAdmin(CleanRelatedWidgetMixin, admin.ModelAdmin):
    form = JobSiteAdminForm
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

    class Media:
        css = {
            "all": ("admin/jobsite_admin.css",)
        }
        js = ("admin/jobsite_admin.js",)

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

    @admin.display(ordering="_status_order", description="Статус")
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
class SearchSignatureAdmin(CleanRelatedWidgetMixin, admin.ModelAdmin):
    form = SearchSignatureAdminForm

    fieldsets = (
        (None, {
            "fields": (
                "job_site",
                "search_text",
                "country",
                "technology",
                "technology_choice",
                "is_active",
            )
        }),
    )

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

    class Media:
        css = {
            "all": ("admin/searchsignature_admin.css",)
        }
        js = ("admin/searchsignature_admin.js",)


# --- SearchTechnology admin and SearchQuery technology links ---
from django.contrib import admin as _admin_for_searchtech

try:
    from .models import SearchTechnology as _SearchTechnology
except Exception:
    _SearchTechnology = None

if _SearchTechnology is not None:
    _SearchTechnology._meta.verbose_name = "Технология"
    _SearchTechnology._meta.verbose_name_plural = "Технологии"

    if not _admin_for_searchtech.site.is_registered(_SearchTechnology):
        @_admin_for_searchtech.register(_SearchTechnology)
        class SearchTechnologyAdmin(_admin_for_searchtech.ModelAdmin):
            list_display = ("sort_order", "name", "code", "is_active")
            list_display_links = ("name",)
            list_editable = ("sort_order", "is_active")
            search_fields = ("name", "code")
            list_filter = ("is_active",)
            ordering = ("sort_order", "name")


try:
    from .models import SearchQuery as _SearchQuery

    _admin_for_searchtech.site._registry[_SearchQuery].change_form_template = (
        "admin/sources/searchquery/change_form.html"
    )
except Exception:
    pass
# --- end SearchTechnology admin and SearchQuery technology links ---


# --- Move Django auth app to bottom in admin sidebar ---
from django.contrib import admin as _admin_for_sidebar_order

if not getattr(_admin_for_sidebar_order.site, "_auth_app_moved_to_bottom", False):
    _original_get_app_list = _admin_for_sidebar_order.site.get_app_list

    def _get_app_list_with_auth_bottom(request, app_label=None):
        app_list = _original_get_app_list(request, app_label)

        normal_apps = []
        auth_apps = []

        for app in app_list:
            if app.get("app_label") == "auth":
                auth_apps.append(app)
            else:
                normal_apps.append(app)

        return normal_apps + auth_apps

    _admin_for_sidebar_order.site.get_app_list = _get_app_list_with_auth_bottom
    _admin_for_sidebar_order.site._auth_app_moved_to_bottom = True
# --- end Move Django auth app to bottom in admin sidebar ---


# --- Custom grouped admin sidebar ---
from django.contrib import admin as _admin_for_custom_sidebar

_admin_site_for_custom_sidebar = _admin_for_custom_sidebar.site


def _job_ads_grouped_admin_app_list(request, app_label=None):
    app_list = _admin_site_for_custom_sidebar._job_ads_base_get_app_list(
        request,
        app_label,
    )

    used = set()

    def model_key(model):
        return (
            model.get("admin_url"),
            model.get("add_url"),
            model.get("name"),
            model.get("object_name"),
        )

    def take_model(display_name):
        for app in app_list:
            for model in app.get("models", []):
                key = model_key(model)

                if key in used:
                    continue

                if model.get("name") == display_name:
                    used.add(key)
                    return model

        return None

    def make_group(app_label_value, group_name, model_names):
        models = []

        for model_name in model_names:
            model = take_model(model_name)
            if model is not None:
                models.append(model)

        if not models:
            return None

        return {
            "name": group_name,
            "app_label": app_label_value,
            "app_url": "",
            "has_module_perms": True,
            "models": models,
        }

    result = []

    custom_groups = [
        (
            "lead_fill",
            "Заполнение лидов",
            [
                "Вакансии",
                "Профили резюме",
            ],
        ),
        (
            "sources",
            "Источники",
            [
                "Поисковые запросы",
                "Сайты вакансий",
            ],
        ),
        (
            "directories",
            "Справочники",
            [
                "Страны",
                "Технологии",
            ],
        ),
    ]

    for custom_app_label, group_name, model_names in custom_groups:
        group = make_group(custom_app_label, group_name, model_names)
        if group is not None:
            result.append(group)

    other_apps = []
    auth_apps = []

    for app in app_list:
        remaining_models = []

        for model in app.get("models", []):
            key = model_key(model)

            if key in used:
                continue

            remaining_models.append(model)

        if not remaining_models:
            continue

        app_copy = dict(app)
        app_copy["models"] = remaining_models

        if app.get("app_label") == "auth":
            auth_apps.append(app_copy)
        else:
            other_apps.append(app_copy)

    result.extend(other_apps)
    result.extend(auth_apps)

    return result


if not hasattr(_admin_site_for_custom_sidebar, "_job_ads_base_get_app_list"):
    _admin_site_for_custom_sidebar._job_ads_base_get_app_list = (
        _admin_site_for_custom_sidebar.get_app_list
    )

_admin_site_for_custom_sidebar.get_app_list = _job_ads_grouped_admin_app_list
# --- end Custom grouped admin sidebar ---

