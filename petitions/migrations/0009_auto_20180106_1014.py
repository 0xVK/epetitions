# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-06 10:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petitions', '0008_auto_20180106_0948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='petition',
            name='status',
            field=models.CharField(choices=[('ACTIVE', 'Збір підписів'), ('CONSIDERATION', 'На розгляді'), ('ANSWERED', 'З відповіддю'), ('REJECTED', 'Не пітримано')], default='ACTIVE', max_length=15),
        ),
    ]
