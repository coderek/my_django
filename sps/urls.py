from django.conf.urls import url, include
from sps import views

'''
urlpatterns = [
    url(r'^messages/?$', views.messages),
    url(r'^videos/?$', views.videos),
    url(r'^news/?$', views.news),
]
'''


urlpatterns = [
    url(r'^', include(views.router.urls)),
]

