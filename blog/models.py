from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Post(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    title = models.CharField(max_length=200)
    body = models.TextField(null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
