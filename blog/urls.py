from django.conf.urls import url
import views

urlpatterns = [
    url(r'^(\d+)/$', views.post, name='post'),
]
