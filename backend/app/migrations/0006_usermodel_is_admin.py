# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-23 23:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_usermodel_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermodel',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
    ]
