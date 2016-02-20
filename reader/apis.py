from django.conf.urls import url
from django.views.generic import View
from django.http import (
    HttpResponseForbidden,
    HttpResponseBadRequest,
    JsonResponse,
    HttpResponseNotFound,
)
from reader.support.feed import fetch_feed
import json
from reader.models import Feed, Entry

# logger = logging.getLogger('__name__')


class FeedsView(View):
    def get(self, request):
        feeds = Feed.feed_list()
        return JsonResponse(feeds, safe=False)

    def post(self, request):
        if not request.user.is_authenticated():
            return HttpResponseForbidden('Must login')
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


def update_entry(request, feed_id, entry_id):
    if request.method == 'PUT':
        data = json.loads(request.body)
        Entry.objects.filter(pk=entry_id).update(**data)
        return JsonResponse(Entry.objects.filter(pk=entry_id).first().as_dict())
    else:
        return HttpResponseBadRequest('Method is not allowed')


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
            if error:
                return HttpResponseBadRequest(error)
            return JsonResponse(feed.as_dict(), safe=False)
        else:
            return JsonResponse(feed.as_dict(), safe=False)
    except Feed.DoesNotExist:
        return HttpResponseNotFound('Resource not found')


urlpatterns = [
    url(r'feeds/?$', FeedsView.as_view()),
    url(r'feeds/(?P<feed_id>\d+)/?$', get_feed),
    url(r'feeds/(?P<feed_id>\d+)/entries/?$', feed_entries),
    url(r'feeds/(?P<feed_id>\d+)/entries/(?P<entry_id>\d+)?$', update_entry),
]
