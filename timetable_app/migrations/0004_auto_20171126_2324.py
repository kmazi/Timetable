# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-26 23:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetable_app', '0003_auto_20171126_0815'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='freetime',
            name='day',
        ),
        migrations.RemoveField(
            model_name='freetime',
            name='lecturer',
        ),
        migrations.DeleteModel(
            name='FreeTime',
        ),
    ]