# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-19 13:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20161219_2116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authorizations',
            name='id',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
    ]
