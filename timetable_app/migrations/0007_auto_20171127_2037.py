# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-27 20:37
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timetable_app', '0006_auto_20171127_2028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='break_time_duration',
            field=models.DurationField(default=datetime.timedelta(0, 3600)),
        ),
    ]
