from datetime import datetime
from django.template.loader import get_template
from django.http import HttpResponse, JsonResponse
from blog.models import Post, Comment
from django.views.generic import View
from rest_framework.views import APIView
from rest_framework.response import (
    Response,
)
from rest_framework import serializers


class BlogView(View):

    def render_to_response(self, tpl, context):
        template = get_template(tpl)
        logged_in = self.request.user.is_authenticated()
        recent_posts = Post.objects.order_by('-created_at').all()[:10]
        context.update({
            'logged_in': logged_in,
            'recent_posts': recent_posts,
        })
        return HttpResponse(template.render(context))


class PostView(BlogView):
    def get(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except:
            return HttpResponse(status=404)

        return self.render_to_response('blog/post.html', {'p': post})


class HomeView(BlogView):
    def get(self, request):
        posts = Post.objects.order_by('-created_at').all()
        return self.render_to_response('blog/home.html', {'posts': posts})


class SearchView(BlogView):
    def get(self, request):
        term = request.GET.get('search_term', '')
        found_posts = Post.objects.order_by('-created_at').filter(
            title__contains=term)
        return self.render_to_response('blog/search.html', {
            'term': term,
            'posts': found_posts,
        })


class NicelyFormattedDate(serializers.DateTimeField):

    def to_representation(self, value):
        return value.strftime('%Y-%m-%d %H:%M:%S%p')


class CommentSerializer(serializers.ModelSerializer):
    created_at = NicelyFormattedDate(required=False)
    class Meta:
        model = Comment
        fields = ('id', 'content', 'email', 'name', 'reply_to', 'post', 'created_at')


class CommentsView(APIView):
    def post(self, request, format=None):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        else:
            return Response(serializer.errors, status=400)

    def get(self, request, format=None):
        comments = Comment.objects.filter(post_id=request.GET.get('post')).order_by('-created_at').all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
