# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-29 23:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20170328_0014'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermodel',
            name='temp_token',
            field=models.CharField(default=b'', max_length=100),
        ),
    ]