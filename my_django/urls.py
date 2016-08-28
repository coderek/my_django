from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from blog.views import HomeView


admin.site.site_header = 'Derek Zeng\' Admin'
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^posts/', include('blog.urls')),
    url(r'^reader/', include('reader.urls')),
    url(r'^oauth/', include('oauth.urls')),
    url(r'^sps/', include('sps.urls')),
    url(r'^api/', include('api.urls')),
    url(r'^$', HomeView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
