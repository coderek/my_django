# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-15 21:26
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OauthToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('access_token', models.CharField(default='', max_length=255)),
                ('expiry_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('oauth_provider', models.CharField(default='', max_length=100)),
                ('third_party_user_id', models.CharField(default='', max_length=255)),
                ('auth_response', models.TextField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
