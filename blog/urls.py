from django.conf.urls import url
from views import (
    CommentsView,
    HomeView,
    SearchView,
    PostView,
)

urlpatterns = [
    url(r'^(\d+)/?$', PostView.as_view(), name='post'),
    url(r'^search', SearchView.as_view()),
    url(r'^api/comments', CommentsView.as_view()),
    url(r'^$', HomeView.as_view(), name='blog'),
]
