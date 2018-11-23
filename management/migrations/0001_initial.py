# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-11-22 13:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('serial', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('author', models.CharField(max_length=200)),
                ('category', models.CharField(max_length=200)),
                ('status', models.CharField(max_length=200)),
                ('cost', models.IntegerField()),
                ('procurement', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Memberships',
            fields=[
                ('id', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('contact', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=200)),
                ('aadhar', models.CharField(max_length=200)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('status', models.CharField(max_length=200)),
                ('fine', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Movies',
            fields=[
                ('serial', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('author', models.CharField(max_length=200)),
                ('category', models.CharField(max_length=200)),
                ('status', models.CharField(max_length=200)),
                ('cost', models.IntegerField()),
                ('procurement', models.DateField(blank=True, null=True)),
            ],
        ),
    ]