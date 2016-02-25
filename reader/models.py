from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Feed(models.Model):
    url = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True)
    etag = models.CharField(max_length=255)
    feed_url = models.CharField(max_length=255, unique=True)
    last_modified = models.DateTimeField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __unicode__(self):
        return self.title

    def as_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'count': self.new_entries_count,
        }

    @property
    def new_entries_count(self):
        oneday = timedelta(days=1)
        return self.entry_set.filter(
            created_at__gte=datetime.today() - oneday).count()

    @classmethod
    def all(cls):
        feeds = cls.objects.all()
        return [f.as_dict() for f in feeds]


class Category(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    entries = models.ManyToManyField('Entry')

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


class Entry(models.Model):
    feed = models.ForeignKey('Feed')
    title = models.CharField(max_length=255)
    url = models.CharField(max_length=255, unique=True)
    author = models.CharField(max_length=255)
    summary = models.TextField(null=True)
    content = models.TextField(null=True)
    published = models.DateTimeField()
    categories = models.ManyToManyField('Category')
    uuid = models.CharField(max_length=255, unique=True)
    is_read = models.BooleanField(default=False)
    is_starred = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __unicode__(self):
        return self.title

    def as_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'summary': self.summary,
            'content': self.content,
            'published': self.published,
            'url': self.url,
            'is_starred': self.is_starred,
        }
