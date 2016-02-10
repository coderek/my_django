from django.conf.urls import url
from django.views.generic import View
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    JsonResponse,
)
from reader.support.feed import fetch_feed
import json
from reader.models import Feed


class FeedsView(View):

    def get(self, request):
        feeds = Feed.feed_list()
        return JsonResponse(feeds, safe=False)

    def post(self, request):
        try:
            body = json.loads(request.body)
            url = body.get('url')
            m, created = fetch_feed(url)
            if created:
                return JsonResponse(m.as_dict(), safe=False)
            else:
                return HttpResponse(status=409, content='Duplicate entry')
        except Exception as e:
            return HttpResponseBadRequest(e)


def feed_entries(request, feed_id):
    feed = Feed.objects.get(pk=feed_id)
    return JsonResponse([e.as_dict() for e in feed.entry_set.all()], safe=False)


urlpatterns = [
    url(r'feeds/?$', FeedsView.as_view()),
    url(r'feeds/(?P<feed_id>\d+)/entries/?$', feed_entries),
]
