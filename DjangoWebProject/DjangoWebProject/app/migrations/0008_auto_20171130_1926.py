# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-11-30 11:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20171130_1925'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='completelm',
            name='complete',
        ),
        migrations.RemoveField(
            model_name='completelm',
            name='lesson',
        ),
        migrations.RemoveField(
            model_name='completelm',
            name='major',
        ),
        migrations.RemoveField(
            model_name='score',
            name='lesson',
        ),
        migrations.RemoveField(
            model_name='score',
            name='student',
        ),
        migrations.DeleteModel(
            name='CompleteLM',
        ),
        migrations.DeleteModel(
            name='Lesson',
        ),
        migrations.DeleteModel(
            name='Score',
        ),
    ]
