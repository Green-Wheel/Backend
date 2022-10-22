# Generated by Django 4.1.1 on 2022-10-12 16:23

from django.db import migrations


def load_initial_data(apps, schema_editor):
    language_model = apps.get_model('chargers', 'CurrentsType')
    language_model.objects.create(
        name="AC"
    )
    language_model.objects.create(
        name="DC"
    )


class Migration(migrations.Migration):
    dependencies = [
        ('chargers', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_initial_data),
    ]