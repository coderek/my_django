from .models import (
    Message, Video, News, Agency
)
from rest_framework import routers, serializers, viewsets


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Message
        fields = ('body', 'user', 'image')

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class VideoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Video
        fields = ('link', 'user', 'title')

class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer


class NewsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = News
        fields = ('title', 'url', 'image_url', 'summary', 'user')

class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer


class AgencySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Agency
        fields = ('name', 'description', 'address', 'contact', 'urls')

class AgencyViewSet(viewsets.ModelViewSet):
    queryset = Agency.objects.all()
    serializer_class = AgencySerializer

router = routers.DefaultRouter()
router.register(r'messages', MessageViewSet)
router.register(r'videos', VideoViewSet)
router.register(r'news', NewsViewSet)
router.register(r'agencies', AgencyViewSet)
