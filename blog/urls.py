from django.conf.urls import url
from views import (
    PostView,
    SearchView,
    HomeView,
)

urlpatterns = [
    url(r'^(\d+)/?$', PostView.as_view(), name='post'),
    url(r'^search', SearchView.as_view()),
    url(r'^$', HomeView.as_view(), name='blog'),
]
