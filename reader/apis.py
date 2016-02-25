import logging

from django.conf.urls import url
from django.http import (
    HttpResponseBadRequest,
    JsonResponse,
)

from reader.models import Entry, Feed
from reader.support.feed import fetch_feed
from reader.support.resource import CollectionAPI, ModelAPI


logger = logging.getLogger('django')


class FeedsView(CollectionAPI):
    model_cls = Feed

    def post(self, request):
        try:
            # import pdb; pdb.set_trace()
            url = request.data.get('url')
            m, error = fetch_feed(url)
            if not error:
                return JsonResponse(m.as_dict(), safe=False)
            else:
                return HttpResponseBadRequest(error)
        except Exception as e:
            return HttpResponseBadRequest(e)


class EntryView(ModelAPI):
    model_cls = Entry

    def prepare(self, request, *args, **kwargs):
        self.feed = Feed.objects.get(pk=kwargs.get('feed_id'))

    def update(self, request, *args, **kwargs):
        Entry.objects.filter(pk=self.instance.id).update(**request.data)
        self.instance.refresh_from_db()
        return JsonResponse(self.instance.as_dict())


class EntriesView(CollectionAPI):
    model_cls = Entry

    def prepare(self, request, *args, **kwargs):
        self.feed = Feed.objects.get(pk=kwargs.get('feed_id'))

    def index(self, request):
        return JsonResponse([
            e.as_dict()
            for e in self.feed.entry_set.all()], safe=False)


class FeedView(ModelAPI):
    model_cls = Feed

    def get(self, request, *args, **kwargs):
        do_refresh = request.data.get('refresh')
        feed = self.instance
        # import pdb; pdb.set_trace()
        if do_refresh:
            feed, error = fetch_feed(feed.feed_url)
            if error:
                return HttpResponseBadRequest(error)
            return JsonResponse(feed.as_dict(), safe=False)
        else:
            return JsonResponse(feed.as_dict(), safe=False)


urlpatterns = [
    # url(r'test/', TestAPIClass.as_view()),
    url(r'feeds/?$', FeedsView.as_view()),
    url(r'feeds/(?P<pk>\d+)/?$', FeedView.as_view()),
    url(r'feeds/(?P<feed_id>\d+)/entries/?$', EntriesView.as_view()),
    url(r'feeds/(?P<feed_id>\d+)/entries/(?P<pk>\d+)?$', EntryView.as_view()),
]
