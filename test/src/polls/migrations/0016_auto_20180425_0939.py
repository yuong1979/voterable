# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-04-25 01:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0015_pollitem_published'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pollitem',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
