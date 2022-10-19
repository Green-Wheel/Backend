# Generated by Django 4.1.1 on 2022-10-19 08:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0002_finishedbookings'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chargers', '0001_initial'),
        ('ratings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ratings',
            fields=[
                ('id_rating', models.AutoField(primary_key=True, serialize=False)),
                ('rate', models.FloatField()),
                ('comment', models.TextField(blank=True, null=True)),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookings.bookings')),
            ],
            options={
                'verbose_name': 'Rating',
                'verbose_name_plural': 'Ratings',
            },
        ),
        migrations.AlterModelOptions(
            name='clientsrating',
            options={},
        ),
        migrations.RemoveField(
            model_name='clientsrating',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='clientsrating',
            name='id',
        ),
        migrations.RemoveField(
            model_name='clientsrating',
            name='rate',
        ),
        migrations.AlterField(
            model_name='clientsrating',
            name='client',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='clientsrating',
            name='ratings_ptr',
            field=models.OneToOneField(auto_created=True, default=1, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ratings.ratings'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='PostRating',
            fields=[
                ('ratings_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ratings.ratings')),
                ('publication', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chargers.publication')),
            ],
            bases=('ratings.ratings',),
        ),
    ]
