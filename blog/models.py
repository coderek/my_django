from __future__ import unicode_literals
import markdown2

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Post(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    published = models.BooleanField(default=False)
    format = models.CharField(max_length=200, null=False, default='markdown')
    title = models.CharField(max_length=200, unique=True)
    body = models.TextField(null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    preview = models.TextField(null=True)

    def __unicode__(self):
        return '<ID:{}> {}'.format(self.id, self.title)

    @property
    def body_snippet(self):
        return self.body[:200] + '...'

    @property
    def body_text(self):
        return markdown2.markdown(self.body)


class Comment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    content = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
