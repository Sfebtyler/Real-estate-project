# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-13 02:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_auto_20161203_0128'),
    ]

    operations = [
        migrations.AddField(
            model_name='home',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='home',
            name='published',
            field=models.BooleanField(default=False),
        ),
    ]
