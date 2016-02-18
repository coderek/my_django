from django.template.loader import get_template
from django.http import HttpResponse
from blog.models import Post
from django.views.generic import View


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
