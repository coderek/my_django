# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-08-28 00:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20160219_0233'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='preview',
            field=models.TextField(null=True),
        ),
    ]