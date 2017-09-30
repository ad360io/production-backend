# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-08-13 17:20
from __future__ import unicode_literals

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qchain_backend', '0002_remove_agent_e_balance'),
    ]

    operations = [
        migrations.AddField(
            model_name='agent',
            name='e_balance',
            field=models.DecimalField(decimal_places=8, default=Decimal('0E-8'), max_digits=12, validators=[django.core.validators.DecimalValidator(12, 8)]),
        ),
        migrations.AlterField(
            model_name='agent',
            name='x_balance',
            field=models.DecimalField(decimal_places=8, default=Decimal('0E-8'), max_digits=12, validators=[django.core.validators.DecimalValidator(12, 8)]),
        ),
    ]
