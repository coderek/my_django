import logging
from django.conf.urls import url
from django.views.generic import View
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    JsonResponse,
    HttpResponseNotFound,
)
from reader.support.feed import fetch_feed
import json
from reader.models import Feed

# logger = logging.getLogger('__name__')

class FeedsView(View):

    def get(self, request):
        feeds = Feed.feed_list()
        return JsonResponse(feeds, safe=False)

    def post(self, request):
        try:
            body = json.loads(request.body)
            url = body.get('url')
            m, error = fetch_feed(url)
            if not error:
                return JsonResponse(m.as_dict(), safe=False)
            else:
                return HttpResponseBadRequest(error)
        except Exception as e:
            return HttpResponseBadRequest(e)


def feed_entries(request, feed_id):
    feed = Feed.objects.get(pk=feed_id)
    return JsonResponse(
        [e.as_dict() for e in feed.entry_set.all()], safe=False)


def get_feed(request, feed_id):
    do_refresh = request.GET.get('refresh')
    try:
        feed = Feed.objects.get(pk=feed_id)
        if do_refresh:
            feed, error = fetch_feed(feed.feed_url)
            return JsonResponse(feed.as_dict(), safe=False)
        else:
            return JsonResponse(feed.as_dict(), safe=False)
    except Feed.DoesNotExist:
        return HttpResponseNotFound('Resource not found')


urlpatterns = [
    url(r'feeds/?$', FeedsView.as_view()),
    url(r'feeds/(?P<feed_id>\d+)/?$', get_feed),
    url(r'feeds/(?P<feed_id>\d+)/entries/?$', feed_entries),
]
