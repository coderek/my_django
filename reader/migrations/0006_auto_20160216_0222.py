# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-16 02:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reader', '0005_auto_20160216_0209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='url',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='entry',
            name='uuid',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
