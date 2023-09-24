# Generated by Django 4.1.7 on 2023-09-24 02:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_week', '0003_alter_appdata_end_date_alter_appdata_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appdata',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='appdata',
            name='start_date',
            field=models.DateField(blank=True, default=datetime.datetime.now),
        ),
    ]
