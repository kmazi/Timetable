# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-01 09:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetable_app', '0007_auto_20171127_2037'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timeslot',
            name='lecturer',
        ),
    ]
