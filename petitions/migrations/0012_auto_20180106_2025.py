# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-06 20:25
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petitions', '0011_auto_20180106_2004'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='petition',
            name='days_left',
        ),
        migrations.RemoveField(
            model_name='petition',
            name='signatures',
        ),
        migrations.AddField(
            model_name='petition',
            name='to_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 1, 16, 20, 25, 23, 710634)),
        ),
    ]