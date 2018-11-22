# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-03-06 01:42
from __future__ import unicode_literals

from django.db import migrations, models
import polls.models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0010_ptype_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ptype',
            name='image',
            field=models.ImageField(blank=True, max_length=2048, null=True, upload_to=polls.models.ptype_image_upload_to),
        ),
    ]
