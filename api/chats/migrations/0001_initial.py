# Generated by Django 4.1.1 on 2022-10-04 16:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=1500)),
                ('read', models.BooleanField(default=False)),
                ('date_time_read', models.DateTimeField(blank=True, null=True)),
                ('date_time_sent', models.DateTimeField(auto_now_add=True)),
                ('user_recived', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_recived', to=settings.AUTH_USER_MODEL)),
                ('user_sent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_sent', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Chat',
                'verbose_name_plural': 'Chats',
            },
        ),
    ]
