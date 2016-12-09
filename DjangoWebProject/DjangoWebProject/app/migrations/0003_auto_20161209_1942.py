# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-09 11:42
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0002_auto_20161208_1523'),
    ]

    operations = [
        migrations.AddField(
            model_name='inspectors',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name=b'\xe5\xae\xa1\xe6\x9f\xa5\xe8\x80\x85'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='students',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name=b'\xe5\xad\xa6\xe7\x94\x9f'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='teachers',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name=b'\xe6\x95\x99\xe5\xb8\x88'),
            preserve_default=False,
        ),
    ]
