# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-10-07 22:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qchain_backend', '0003_auto_20171007_2135'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='adlisting',
            name='asking_rate',
        ),
    ]
