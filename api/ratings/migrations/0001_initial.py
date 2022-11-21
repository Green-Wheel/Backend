# Generated by Django 4.1.1 on 2022-11-21 10:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bookings', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ratings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.FloatField()),
                ('comment', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookings.bookings')),
            ],
            options={
                'verbose_name': 'Rating',
                'verbose_name_plural': 'Ratings',
            },
        ),
        migrations.CreateModel(
            name='ClientsRating',
            fields=[
                ('ratings_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ratings.ratings')),
            ],
            options={
                'verbose_name': 'Client Rating',
                'verbose_name_plural': 'Clients Ratings',
            },
            bases=('ratings.ratings',),
        ),
        migrations.CreateModel(
            name='PostRating',
            fields=[
                ('ratings_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ratings.ratings')),
            ],
            options={
                'verbose_name': 'Publication Rating',
                'verbose_name_plural': 'Publications Ratings',
            },
            bases=('ratings.ratings',),
        ),
    ]
