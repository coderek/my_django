from django.conf.urls import url
from sps import views

urlpatterns = [
    url(r'^messages/?$', views.messages),
    url(r'^videos/?$', views.videos),
    url(r'^news/?$', views.news),
]
