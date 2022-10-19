# Generated by Django 4.1.1 on 2022-10-19 08:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ratings', '0002_ratings_alter_clientsrating_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientsrating',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
