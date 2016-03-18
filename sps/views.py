from .models import Message, Video, News
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
        model = Message
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


router = routers.DefaultRouter()
router.register(r'messages', MessageViewSet)
router.register(r'videos', VideoViewSet)
router.register(r'news', NewsViewSet)
