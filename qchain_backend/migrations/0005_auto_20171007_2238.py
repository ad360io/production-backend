# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-10-07 22:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qchain_backend', '0004_remove_adlisting_asking_rate'),
    ]

    operations = [
        migrations.RenameField(
            model_name='adlisting',
            old_name='cpc',
            new_name='cpm',
        ),
    ]
