# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-22 00:48
from __future__ import unicode_literals

import django.contrib.auth.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='usermodel',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
