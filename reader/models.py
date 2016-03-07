from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.db import models


class Resource(object):
    def as_dict(self):
        return {}

    def _as_dict(self):
        d = self.as_dict()
        res = {
            'id': self.id,
        }
        res.update(d)
        return res

    @classmethod
    def all(cls):
        collection = cls.objects.all()
        return [c._as_dict() for c in collection]


class Feed(Resource, models.Model):
    url = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True)
    etag = models.CharField(max_length=255)
    feed_url = models.CharField(max_length=255, unique=True)
    last_modified = models.DateTimeField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(
        'Category', models.SET_DEFAULT, default=1, related_name='feeds')

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __unicode__(self):
        return u'{} ({})'.format(self.title, self.category.name)

    def as_dict(self):
        return {
            'title': self.title,
            'description': self.description,
            'count': self.new_entries_count,
        }

    @property
    def new_entries_count(self):
        oneday = timedelta(days=1)
        return self.entries.filter(
            created_at__gte=datetime.today() - oneday).count()


class Tag(Resource, models.Model):
    name = models.CharField(max_length=255)
    entries = models.ManyToManyField('Entry')

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __unicode__(self):
        return u'{}: {} entries'.format(self.name, self.entries.count())


class Category(Resource, models.Model):
    name = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __unicode__(self):
        return u'{}: {} feeds'.format(self.name, self.feeds.count())

    def as_dict(self):
        return {
            'name': self.name,
            'count': self.feeds.count(),
        }


class Entry(Resource, models.Model):
    feed = models.ForeignKey('Feed', related_name='entries')
    title = models.CharField(max_length=255)
    url = models.CharField(max_length=255, unique=True)
    author = models.CharField(max_length=255)
    summary = models.TextField(null=True)
    content = models.TextField(null=True)
    published = models.DateTimeField()
    uuid = models.CharField(max_length=255, unique=True)
    is_read = models.BooleanField(default=False)
    is_starred = models.BooleanField(default=False)
    tags = models.ManyToManyField('Tag')

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __unicode__(self):
        return self.title

    def as_dict(self):
        return {
            'title': self.title,
            'summary': self.summary,
            'content': self.content,
            'published': self.published,
            'url': self.url,
            'is_starred': self.is_starred,
        }
