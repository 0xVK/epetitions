# Generated by Django 2.0.2 on 2018-02-27 13:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petitions', '0016_auto_20180219_1015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='petition',
            name='to_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 3, 29, 15, 49, 44, 284232), verbose_name='Кінцева дата'),
        ),
    ]
