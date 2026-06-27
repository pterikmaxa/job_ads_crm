from django import template
from django.apps import apps
from django.db.models import Count, Sum

register = template.Library()


def get_first_model(candidates):
    for app_label, model_name in candidates:
        try:
            return apps.get_model(app_label, model_name)
        except LookupError:
            continue
    return None


def field_names(model):
    if model is None:
        return set()
    return {field.name for field in model._meta.fields}


def active_qs(model):
    qs = model.objects.all()
    names = field_names(model)

    if "active" in names:
        return qs.filter(active=True)

    if "is_active" in names:
        return qs.filter(is_active=True)

    return qs


def active_count(model):
    if model is None:
        return 0
    return active_qs(model).count()


def total_count(model):
    if model is None:
        return 0
    return model.objects.count()


def sites_today_plan(site_model):
    if site_model is None:
        return "0 / 0"

    names = field_names(site_model)
    qs = active_qs(site_model)

    processed_today = 0
    daily_plan = 0

    if "processed_today" in names:
        processed_today = qs.aggregate(value=Sum("processed_today"))["value"] or 0

    if "daily_plan" in names:
        daily_plan = qs.aggregate(value=Sum("daily_plan"))["value"] or 0

    return f"{processed_today} / {daily_plan}"


def normalize_color_status(value):
    if value is None or value == "":
        return "Без статуса"

    text = str(value).strip()

    labels = {
        "red": "Проблема",
        "problem": "Проблема",
        "проблема": "Проблема",

        "yellow": "Внимание",
        "attention": "Внимание",
        "warning": "Внимание",
        "внимание": "Внимание",

        "green": "ОК",
        "ok": "ОК",
        "ок": "ОК",

        "blue": "Сломан",
        "broken": "Сломан",
        "сломано": "Сломан",
        "сломан": "Сломан",
    }

    return labels.get(text.lower(), text)


def site_status_summary(site_model):
    if site_model is None:
        return "—"

    names = field_names(site_model)
    qs = active_qs(site_model)

    if "color_status" not in names:
        return f"Всего: {qs.count()}"

    rows = (
        qs.values("color_status")
        .annotate(count=Count("id"))
        .order_by("color_status")
    )

    counts = {}

    for row in rows:
        label = normalize_color_status(row["color_status"])
        counts[label] = counts.get(label, 0) + row["count"]

    order = [
        "Проблема",
        "Внимание",
        "ОК",
        "Сломан",
        "Без статуса",
    ]

    parts = []

    for label in order:
        if label in counts:
            parts.append(f"{label}: {counts[label]}")

    for label, count in counts.items():
        if label not in order:
            parts.append(f"{label}: {count}")

    return " / ".join(parts) if parts else "—"


@register.simple_tag
def today_task_rows():
    JobSite = get_first_model([
        ("sources", "JobSite"),
    ])

    SearchSignature = get_first_model([
        ("sources", "SearchSignature"),
        ("sources", "SearchQuery"),
    ])

    JobPost = get_first_model([
        ("vacancies", "JobPost"),
    ])

    return [
        {
            "name": "Сайты вакансий",
            "current": sites_today_plan(JobSite),
            "total": site_status_summary(JobSite),
        },
        {
            "name": "Поисковые запросы",
            "current": active_count(SearchSignature),
            "total": total_count(SearchSignature),
        },
        {
            "name": "Вакансии",
            "current": active_count(JobPost),
            "total": total_count(JobPost),
        },
    ]
