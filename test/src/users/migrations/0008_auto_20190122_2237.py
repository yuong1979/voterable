# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-01-22 14:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_puser_referralid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='puser',
            name='referralid',
            field=models.CharField(default='None', max_length=6, null=True),
        ),
    ]
