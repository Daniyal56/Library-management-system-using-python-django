# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-11-22 14:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memberships',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
