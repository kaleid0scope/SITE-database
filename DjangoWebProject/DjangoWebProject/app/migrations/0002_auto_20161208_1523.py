# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-08 07:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Competition',
            fields=[
                ('ProjectNum', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('rankNum', models.PositiveIntegerField()),
                ('ProjectTime', models.DateField()),
                ('SupportText', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='CompetitionRank',
            fields=[
                ('rankNum', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('Level', models.CharField(max_length=20)),
                ('rank', models.SmallIntegerField()),
                ('score', models.SmallIntegerField()),
                ('startingTime', models.DateField()),
                ('CompleteNum', models.PositiveIntegerField()),
                ('inspectorNum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Inspectors')),
            ],
        ),
        migrations.CreateModel(
            name='Exchange',
            fields=[
                ('ProjectNum', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('rankNum', models.PositiveIntegerField()),
                ('ProjectName', models.CharField(max_length=20)),
                ('targetName', models.CharField(max_length=20)),
                ('startTime', models.DateField()),
                ('endTime', models.DateField()),
                ('ProjectContent', models.TextField()),
                ('SupportText', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ExchangeRank',
            fields=[
                ('rankNum', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=50)),
                ('nature', models.CharField(max_length=20)),
                ('score', models.SmallIntegerField()),
                ('startingTime', models.DateField()),
                ('CompleteNum', models.PositiveIntegerField()),
                ('inspectorNum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Inspectors')),
            ],
        ),
        migrations.CreateModel(
            name='IdeologyConstruction',
            fields=[
                ('ProjectNum', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('rankNum', models.PositiveIntegerField()),
                ('SupportText', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='IdeologyConstructionRank',
            fields=[
                ('rankNum', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=20)),
                ('organizer', models.CharField(max_length=50)),
                ('startingTime', models.DateField()),
                ('Location', models.CharField(max_length=50)),
                ('Content', models.TextField()),
                ('score', models.SmallIntegerField()),
                ('CompleteNum', models.PositiveIntegerField()),
                ('inspectorNum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Inspectors')),
            ],
        ),
        migrations.CreateModel(
            name='Internship',
            fields=[
                ('ProjectNum', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('rankNum', models.PositiveIntegerField()),
                ('name', models.CharField(max_length=20)),
                ('startingTime', models.DateField()),
                ('location', models.CharField(max_length=50)),
                ('job', models.CharField(max_length=50)),
                ('contribution', models.TextField()),
                ('report', models.TextField()),
                ('appraisal', models.TextField()),
                ('SupportText', models.TextField()),
                ('score', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='InternshipRank',
            fields=[
                ('rankNum', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=50)),
                ('startingTime', models.DateField()),
                ('score', models.SmallIntegerField()),
                ('CompleteNum', models.PositiveIntegerField()),
                ('inspectorNum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Inspectors')),
            ],
        ),
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('ProjectNum', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('rankNum', models.PositiveIntegerField()),
                ('SupportText', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='LectureRank',
            fields=[
                ('rankNum', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=20)),
                ('organizer', models.CharField(max_length=50)),
                ('speaker', models.CharField(max_length=50)),
                ('startingTime', models.DateField()),
                ('Location', models.CharField(max_length=50)),
                ('Content', models.TextField()),
                ('score', models.SmallIntegerField()),
                ('CompleteNum', models.PositiveIntegerField()),
                ('inspectorNum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Inspectors')),
            ],
        ),
        migrations.CreateModel(
            name='Paper',
            fields=[
                ('ProjectNum', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('rankNum', models.PositiveIntegerField()),
                ('ProjectName', models.CharField(max_length=20)),
                ('ProjectTime', models.DateField()),
                ('SupportText', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='PaperRank',
            fields=[
                ('rankNum', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('JournalName', models.CharField(max_length=50)),
                ('Level', models.CharField(max_length=20)),
                ('AuthorRanking', models.SmallIntegerField()),
                ('score', models.SmallIntegerField()),
                ('startingTime', models.DateField()),
                ('CompleteNum', models.PositiveIntegerField()),
                ('inspectorNum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Inspectors')),
            ],
        ),
        migrations.CreateModel(
            name='SchoolActivity',
            fields=[
                ('ProjectNum', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('rankNum', models.PositiveIntegerField()),
                ('SupportText', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='SchoolActivityRank',
            fields=[
                ('rankNum', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=20)),
                ('sponsor', models.CharField(max_length=50)),
                ('organizer', models.CharField(max_length=50)),
                ('startingTime', models.DateField()),
                ('awardLevel', models.CharField(max_length=50)),
                ('score', models.SmallIntegerField()),
                ('CompleteNum', models.PositiveIntegerField()),
                ('inspectorNum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Inspectors')),
            ],
        ),
        migrations.CreateModel(
            name='StudentCadre',
            fields=[
                ('ProjectNum', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('rankNum', models.PositiveIntegerField()),
                ('startTime', models.DateField()),
                ('endTime', models.DateField()),
                ('opinions', models.TextField()),
                ('SupportText', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='StudentCadreRank',
            fields=[
                ('rankNum', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('organizitionType', models.CharField(max_length=50)),
                ('organizitionName', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=20)),
                ('score', models.SmallIntegerField()),
                ('CompleteNum', models.PositiveIntegerField()),
                ('inspectorNum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Inspectors')),
            ],
        ),
        migrations.CreateModel(
            name='Volunteering',
            fields=[
                ('ProjectNum', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('rankNum', models.PositiveIntegerField()),
                ('SupportText', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='VolunteeringRank',
            fields=[
                ('rankNum', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('organizer', models.CharField(max_length=50)),
                ('startingTime', models.DateField()),
                ('Location', models.CharField(max_length=50)),
                ('volunteerTime', models.PositiveIntegerField()),
                ('Content', models.TextField()),
                ('score', models.SmallIntegerField()),
                ('CompleteNum', models.PositiveIntegerField()),
                ('inspectorNum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Inspectors')),
            ],
        ),
        migrations.RemoveField(
            model_name='students',
            name='photo',
        ),
        migrations.AddField(
            model_name='researchproject',
            name='SupportText',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='classscore',
            name='StudentNum',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Students'),
        ),
        migrations.AlterField(
            model_name='researchproject',
            name='ProjectTime',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='researchproject',
            name='StudentNum',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Students'),
        ),
        migrations.AlterField(
            model_name='researchprojectrank',
            name='startingTime',
            field=models.DateField(),
        ),
        migrations.AddField(
            model_name='volunteering',
            name='StudentNum',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Students'),
        ),
        migrations.AddField(
            model_name='volunteering',
            name='inspectorNum',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Inspectors'),
        ),
        migrations.AddField(
            model_name='studentcadre',
            name='StudentNum',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Students'),
        ),
        migrations.AddField(
            model_name='studentcadre',
            name='inspectorNum',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Inspectors'),
        ),
        migrations.AddField(
            model_name='schoolactivity',
            name='StudentNum',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Students'),
        ),
        migrations.AddField(
            model_name='schoolactivity',
            name='inspectorNum',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Inspectors'),
        ),
        migrations.AddField(
            model_name='paper',
            name='StudentNum',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Students'),
        ),
        migrations.AddField(
            model_name='paper',
            name='inspectorNum',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Inspectors'),
        ),
        migrations.AddField(
            model_name='lecture',
            name='StudentNum',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Students'),
        ),
        migrations.AddField(
            model_name='lecture',
            name='inspectorNum',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Inspectors'),
        ),
        migrations.AddField(
            model_name='internship',
            name='StudentNum',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Students'),
        ),
        migrations.AddField(
            model_name='internship',
            name='inspectorNum',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Inspectors'),
        ),
        migrations.AddField(
            model_name='ideologyconstruction',
            name='StudentNum',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Students'),
        ),
        migrations.AddField(
            model_name='ideologyconstruction',
            name='inspectorNum',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Inspectors'),
        ),
        migrations.AddField(
            model_name='exchange',
            name='StudentNum',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Students'),
        ),
        migrations.AddField(
            model_name='exchange',
            name='inspectorNum',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Inspectors'),
        ),
        migrations.AddField(
            model_name='competition',
            name='StudentNum',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Students'),
        ),
        migrations.AddField(
            model_name='competition',
            name='inspectorNum',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Inspectors'),
        ),
    ]
