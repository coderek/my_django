from django.conf.urls import url
from django.views.generic import View
from django.http import HttpResponse, HttpResponseBadRequest
from reader.support.feed import fetch_feed
import json


class FeedsView(View):
    def post(self, request):
        try:
            body = json.loads(request.body)
            url = body.get('url')
            d = fetch_feed(url)
            return HttpResponse(d.title)
        except:
            return HttpResponseBadRequest('Very bad')


urlpatterns = [
    url(r'feeds', FeedsView.as_view())
]
