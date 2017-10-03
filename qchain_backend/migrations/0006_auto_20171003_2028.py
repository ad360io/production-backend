# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-10-03 20:28
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qchain_backend', '0005_auto_20171001_2225'),
    ]

    operations = [
        migrations.AddField(
            model_name='adlisting',
            name='cpc',
            field=models.DecimalField(decimal_places=8, default=0, max_digits=12, validators=[django.core.validators.MinValueValidator(0), django.core.validators.DecimalValidator(12, 8)]),
        ),
        migrations.AddField(
            model_name='adlisting',
            name='cpi',
            field=models.DecimalField(decimal_places=8, default=0, max_digits=12, validators=[django.core.validators.MinValueValidator(0), django.core.validators.DecimalValidator(12, 8)]),
        ),
        migrations.AddField(
            model_name='requestforadv',
            name='cpc',
            field=models.DecimalField(decimal_places=8, default=0, max_digits=12, validators=[django.core.validators.MinValueValidator(0), django.core.validators.DecimalValidator(12, 8)]),
        ),
        migrations.AddField(
            model_name='requestforadv',
            name='cpi',
            field=models.DecimalField(decimal_places=8, default=0, max_digits=12, validators=[django.core.validators.MinValueValidator(0), django.core.validators.DecimalValidator(12, 8)]),
        ),
        migrations.AlterField(
            model_name='adlisting',
            name='msg',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='agent',
            name='bio',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='requestforadv',
            name='msg',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='website',
            name='description',
            field=models.CharField(max_length=300),
        ),
    ]