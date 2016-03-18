from __future__ import unicode_literals
from django.contrib import admin

from django.db import models
from my_django.support.model import Model


class Message(Model):
    body = models.TextField()
    image = models.ImageField(
        upload_to='uploads/%Y/%m/%d/', max_length=255, null=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)


class Video(Model):
    title = models.CharField(max_length=255, default='')
    link = models.TextField()
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)


class News(Model):
    title = models.CharField(max_length=255, default='')
    url = models.CharField(max_length=255, default='')
    image_url = models.CharField(max_length=255, default='')
    summary = models.TextField()
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

admin.site.register(Message)
admin.site.register(Video)
admin.site.register(News)
