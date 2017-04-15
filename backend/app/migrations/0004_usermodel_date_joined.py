# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-23 00:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20170322_2354'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermodel',
            name='date_joined',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined'),
        ),
    ]