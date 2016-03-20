from __future__ import unicode_literals
from django.contrib import admin

from django.db import models
from my_django.support.model import Model


class Message(Model):
    body = models.TextField()
    image = models.ImageField(
        upload_to='uploads/%Y/%m/%d/', max_length=255, null=True)

    def __unicode__(self):
        return 'Message:{}'.format(self.id)


class Video(Model):
    title = models.CharField(max_length=255, default='')
    link = models.TextField()

    def __unicode__(self):
        return 'Video:{}'.format(self.id)


class News(Model):

    class Meta:
        verbose_name_plural = 'News'

    title = models.CharField(max_length=255, default='')
    url = models.CharField(max_length=255, default='')
    image_url = models.CharField(max_length=255, default='')
    summary = models.TextField()

    def __unicode__(self):
        return 'News:{}'.format(self.id)


class Agency(Model):

    class Meta:
        verbose_name_plural = 'Agencies'

    name = models.CharField(max_length=255, default='')
    description = models.TextField()
    address = models.TextField()
    contact = models.TextField()
    urls = models.TextField()
    image = models.ImageField(
        upload_to='uploads/%Y/%m/%d/', max_length=255, null=True)


    def __unicode__(self):
        return 'Agency:{}'.format(self.id)


admin.site.register(Message)
admin.site.register(Video)
admin.site.register(News)
admin.site.register(Agency)
