# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-05 02:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reader', '0002_auto_20160205_0204'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='entries',
            field=models.ManyToManyField(to='reader.Entry'),
        ),
        migrations.RemoveField(
            model_name='entry',
            name='categories',
        ),
        migrations.AddField(
            model_name='entry',
            name='categories',
            field=models.ManyToManyField(to='reader.Category'),
        ),
    ]