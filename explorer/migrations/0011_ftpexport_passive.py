# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-29 15:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('explorer', '0010_ftpexport'),
    ]

    operations = [
        migrations.AddField(
            model_name='ftpexport',
            name='passive',
            field=models.BooleanField(default=False),
        ),
    ]
