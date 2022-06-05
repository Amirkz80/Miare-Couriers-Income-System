# Generated by Django 4.0.5 on 2022-06-03 15:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wages_manager', '0003_weeklywage_unique_courier_and_saturday_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailywage',
            name='date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='trip',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='wageincrement',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='wagereduction',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]