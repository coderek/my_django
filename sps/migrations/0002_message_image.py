# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-17 02:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sps', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='image',
            field=models.ImageField(max_length=255, null=True, upload_to='uploads/%Y/%m/%d/'),
        ),
    ]