from django.conf.urls import url
import views

urlpatterns = [
    url(r'^(\d+)/?$', views.post, name='post'),
    url(r'^search', views.search),
    url(r'^$', views.home, name='blog'),
]
