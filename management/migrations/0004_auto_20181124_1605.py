# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-11-24 10:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0003_active_issues'),
    ]

    operations = [
        migrations.RenameField(
            model_name='active_issues',
            old_name='member_id',
            new_name='id',
        ),
    ]
