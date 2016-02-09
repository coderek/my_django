from django.conf.urls import include, url
import views

urlpatterns = [
    url(r'^$', views.home, name='reader'),
    url(r'api/', include('reader.apis')),
]
