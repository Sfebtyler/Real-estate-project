# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-03 01:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20161203_0038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='home',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images'),
        ),
    ]
