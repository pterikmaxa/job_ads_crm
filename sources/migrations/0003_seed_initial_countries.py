from django.db import migrations


INITIAL_COUNTRIES = (
    ("Germany", "DE"),
    ("Ukraine", "UA"),
)


def seed_initial_countries(apps, schema_editor):
    Country = apps.get_model("sources", "Country")

    for name, code in INITIAL_COUNTRIES:
        Country.objects.update_or_create(
            code=code,
            defaults={"name": name, "is_active": True},
        )


class Migration(migrations.Migration):

    dependencies = [
        ("sources", "0002_country_alter_jobsite_country_and_more"),
    ]

    operations = [
        migrations.RunPython(seed_initial_countries, migrations.RunPython.noop),
    ]
