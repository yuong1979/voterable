# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-05-17 06:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0011_ranking_add_days'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ranking',
            name='high_score',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=100, null=True),
        ),
        migrations.AlterField(
            model_name='ranking',
            name='low_score',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=100, null=True),
        ),
    ]
