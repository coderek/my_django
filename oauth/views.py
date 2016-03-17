from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.forms import ModelForm
import json
from .models import OauthToken


def facebook(request):
    return render(request, 'facebook.html', {
        'is_user_logged_in': request.user.is_authenticated()
    })


def get_oauth_info(data):
    # user access token to get user information
    pass


def facebook_auth(request):
    pass
