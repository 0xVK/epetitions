# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-06 17:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='photo',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='status',
        ),
        migrations.AddField(
            model_name='profile',
            name='fb_link',
            field=models.URLField(blank=True, null=True, verbose_name='Посилання на профіль в ФБ'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='fb_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
