# Generated by Django 2.2.1 on 2019-12-06 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('holidays', '0002_remove_flight_arr_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='flight',
            name='arrival',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='flight',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
