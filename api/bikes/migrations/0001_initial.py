# Generated by Django 4.1.1 on 2022-11-19 13:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('chargers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BikeTypes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True, unique=True)),
            ],
            options={
                'verbose_name': 'BikeType',
                'verbose_name_plural': 'BikeTypes',
            },
        ),
        migrations.CreateModel(
            name='Bikes',
            fields=[
                ('publication_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='chargers.publication')),
                ('power', models.FloatField(null=True)),
                ('price', models.FloatField(null=True)),
                ('bike_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bikes.biketypes')),
            ],
            options={
                'verbose_name': 'Bike',
                'verbose_name_plural': 'Bikes',
            },
            bases=('chargers.publication',),
        ),
    ]
