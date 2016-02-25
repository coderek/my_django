from django.conf.urls import include, url

from views import HomeView

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='reader'),
    url(r'api/', include('reader.apis')),
]
