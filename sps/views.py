from .models import (
    Message, Video, News, Agency
)
from rest_framework import routers, serializers, viewsets


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'created_at', 'body', 'user', 'image')

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.order_by('-created_at')
    serializer_class = MessageSerializer


class VideoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Video
        fields = ('id', 'created_at', 'link', 'user', 'title')

class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.order_by('-created_at')
    serializer_class = VideoSerializer


class NewsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = News
        fields = ('id', 'created_at', 'title', 'url', 'image_url', 'summary', 'user')

class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.order_by('-created_at')
    serializer_class = NewsSerializer


class AgencySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Agency
        fields = ('id', 'created_at', 'name', 'description', 'address', 'contact', 'urls', 'image')

class AgencyViewSet(viewsets.ModelViewSet):
    queryset = Agency.objects.order_by('-created_at')
    serializer_class = AgencySerializer

router = routers.DefaultRouter()
router.register(r'messages', MessageViewSet)
router.register(r'videos', VideoViewSet)
router.register(r'news', NewsViewSet)
router.register(r'agencies', AgencyViewSet)
