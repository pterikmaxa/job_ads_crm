from django.db import migrations


STATUS_PROBLEM = "problem"
STATUS_ATTENTION = "attention"
STATUS_OK = "ok"
STATUS_INACTIVE = "inactive"


def calculate_color_status(daily_plan, processed_today):
    if daily_plan == 0:
        return STATUS_INACTIVE
    if processed_today == 0:
        return STATUS_PROBLEM
    if processed_today < daily_plan:
        return STATUS_ATTENTION
    return STATUS_OK


def recalculate_jobsite_color_status(apps, schema_editor):
    JobSite = apps.get_model("sources", "JobSite")

    for job_site in JobSite.objects.all():
        job_site.color_status = calculate_color_status(
            job_site.daily_plan,
            job_site.processed_today,
        )
        job_site.save(update_fields=["color_status"])


class Migration(migrations.Migration):

    dependencies = [
        ("sources", "0004_alter_jobsite_color_status"),
    ]

    operations = [
        migrations.RunPython(recalculate_jobsite_color_status, migrations.RunPython.noop),
    ]
