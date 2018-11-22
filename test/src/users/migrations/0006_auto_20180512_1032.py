# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-05-12 02:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20180430_1405'),
    ]

    operations = [
        migrations.AddField(
            model_name='puser',
            name='memberp',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='puser',
            name='subenddatep',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='puser',
            name='substartdatep',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
