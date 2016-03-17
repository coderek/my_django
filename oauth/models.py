from __future__ import unicode_literals
from django.utils import timezone

from django.db import models


class OauthToken(models.Model):
    user = models.ForeignKey('auth.user')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    # Access token
    access_token = models.CharField(max_length=255, null=False, default='')

    expiry_date = models.DateTimeField(default=timezone.now)

    # provider, Facebook/Google/Self
    oauth_provider = models.CharField(max_length=100, null=False, default='')

    third_party_user_id = models.CharField(
        max_length=255, null=False, default='')

    auth_response = models.TextField(null=True)
