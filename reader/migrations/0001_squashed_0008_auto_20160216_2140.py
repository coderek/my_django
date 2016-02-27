# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-27 15:13
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [('reader', '0001_initial'), ('reader', '0002_auto_20160205_0204'), ('reader', '0003_auto_20160205_0208'), ('reader', '0004_auto_20160216_0206'), ('reader', '0005_auto_20160216_0209'), ('reader', '0006_auto_20160216_0222'), ('reader', '0007_auto_20160216_0313'), ('reader', '0008_auto_20160216_2140')]

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('url', models.CharField(max_length=100)),
                ('author', models.CharField(max_length=100)),
                ('summary', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('published', models.DateTimeField()),
                ('uuid', models.CharField(max_length=100)),
                ('is_read', models.BooleanField(default=False)),
                ('is_starred', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('categories', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reader.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(null=True)),
                ('etag', models.CharField(max_length=255)),
                ('feed_url', models.CharField(max_length=255, unique=True)),
                ('last_modified', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='entry',
            name='feed',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reader.Feed'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='summary',
            field=models.TextField(),
        ),
        migrations.AddField(
            model_name='category',
            name='entries',
            field=models.ManyToManyField(to=b'reader.Entry'),
        ),
        migrations.RemoveField(
            model_name='entry',
            name='categories',
        ),
        migrations.AddField(
            model_name='entry',
            name='categories',
            field=models.ManyToManyField(to=b'reader.Category'),
        ),
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
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='entry',
            name='author',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='entry',
            name='title',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='entry',
            name='url',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='entry',
            name='uuid',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='entry',
            name='content',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='entry',
            name='summary',
            field=models.TextField(null=True),
        ),
    ]
