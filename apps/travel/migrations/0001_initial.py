# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-21 14:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('destination', models.CharField(max_length=255)),
                ('desc', models.CharField(max_length=255)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('username', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='trip',
            name='joiners',
            field=models.ManyToManyField(related_name='joinedtrips', to='travel.User'),
        ),
        migrations.AddField(
            model_name='trip',
            name='planner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plannedtrips', to='travel.User'),
        ),
    ]
