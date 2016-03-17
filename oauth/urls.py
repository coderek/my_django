from django.conf.urls import url
from oauth.views import (
    facebook,
    facebook_auth,
)

urlpatterns = [
    url(r'^facebook$', facebook),
    url(r'^facebook/auth$', facebook_auth),
]
