from django.http import JsonResponse
from .models import Message, Video, News


def messages(request):
    return JsonResponse(Message.all(), safe=False)


def videos(request):
    return JsonResponse(Video.all(), safe=False)


def news(request):
    return JsonResponse(News.all(), safe=False)
