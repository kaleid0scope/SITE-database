# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-11-29 14:16
from __future__ import unicode_literals

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_delete_plan'),
    ]

    operations = [
        migrations.AddField(
            model_name='major',
            name='plan',
            field=models.FileField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location=b'/media'), upload_to=b'', verbose_name=b'\xe5\x9f\xb9\xe5\x85\xbb\xe6\x96\xb9\xe6\xa1\x88'),
        ),
    ]