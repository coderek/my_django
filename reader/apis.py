import logging

from django.conf.urls import url
from django.http import (
    HttpResponseBadRequest,
)

from reader.models import Category, Entry, Feed
from reader.support.feed import fetch_feed
from reader.support.resource import (
    CollectionAPI,
    ModelAPI,
)


logger = logging.getLogger('django')


class FeedsView(CollectionAPI):
    model_cls = Feed

    def post(self, request):
        try:
            url = request.data.get('url')
            if Feed.objects.filter(feed_url=url).exists():
                return HttpResponseBadRequest('Already exists!')
            try:
                m = fetch_feed(url)
                return self.json_response(m.as_dict())
            except Exception as e:
                return HttpResponseBadRequest(e)
        except Exception as e:
            return HttpResponseBadRequest(e)


class EntryView(ModelAPI):
    model_cls = Entry

    def prepare(self, request, *args, **kwargs):
        self.feed = Feed.objects.get(pk=kwargs.get('feed_id'))

    def update(self, request, *args, **kwargs):
        Entry.objects.filter(pk=self.instance.id).update(**request.data)
        self.instance.refresh_from_db()
        return self.json_response(self.instance.as_dict())


class EntriesView(CollectionAPI):
    model_cls = Entry

    def prepare(self, request, *args, **kwargs):
        self.feed = Feed.objects.get(pk=kwargs.get('feed_id'))

    def index(self, request):
        return self.json_response(e.as_dict() for e in self.feed.entries.order_by('-created_at')[:100])


class FeedView(ModelAPI):
    model_cls = Feed

    def get(self, request, *args, **kwargs):
        do_refresh = request.data.get('refresh')
        feed = self.instance
        # import pdb; pdb.set_trace()
        if do_refresh:
            try:
                feed = fetch_feed(feed.feed_url)
            except Exception as e:
                return HttpResponseBadRequest(e)

        return self.json_response(feed.as_dict())


class CategoryView(CollectionAPI):
    model_cls = Category

urlpatterns = [
    # url(r'test/', TestAPIClass.as_view()),
    url(r'categories/?$', CategoryView.as_view()),
    url(r'feeds/?$', FeedsView.as_view()),
    url(r'feeds/(?P<pk>\d+)/?$', FeedView.as_view()),
    url(r'feeds/(?P<feed_id>\d+)/entries/?$', EntriesView.as_view()),
    url(r'feeds/(?P<feed_id>\d+)/entries/(?P<pk>\d+)?$', EntryView.as_view()),
]
