# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-10-01 22:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qchain_backend', '0004_adlisting'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='name',
            field=models.CharField(max_length=80, verbose_name=b'Ad Name'),
        ),
        migrations.AlterField(
            model_name='adlisting',
            name='name',
            field=models.CharField(max_length=80),
        ),
        migrations.AlterField(
            model_name='adspace',
            name='name',
            field=models.CharField(max_length=80, verbose_name=b'Adspace Name'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='currency',
            field=models.CharField(choices=[(b'eqc', b'EQC'), (b'xqc', b'XQC')], max_length=80),
        ),
        migrations.AlterField(
            model_name='contract',
            name='name',
            field=models.CharField(max_length=80),
        ),
        migrations.AlterField(
            model_name='requestforadv',
            name='name',
            field=models.CharField(max_length=80),
        ),
        migrations.AlterField(
            model_name='website',
            name='name',
            field=models.CharField(max_length=80),
        ),
    ]
