# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-11-09 01:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_auto_20171109_0944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pollitem',
            name='imgatt',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='pollitem',
            name='textatt',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
