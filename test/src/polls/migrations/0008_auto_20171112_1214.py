# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-11-12 04:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0007_auto_20171109_0957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ptype',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
