from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Feed(models.Model):
    url = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    etag = models.CharField(max_length=100)
    feed_url = models.CharField(max_length=100, unique=True)
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
        }

    @classmethod
    def feed_list(cls):
        feeds = cls.objects.all()
        return [
            f.as_dict()
            for f in feeds
        ]


class Category(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    entries = models.ManyToManyField('Entry')

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


class Entry(models.Model):
    feed = models.ForeignKey('Feed')
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=100, unique=True)
    author = models.CharField(max_length=100)
    summary = models.TextField()
    content = models.TextField()
    published = models.DateTimeField()
    categories = models.ManyToManyField('Category')
    uuid = models.CharField(max_length=100, unique=True)
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
        }
