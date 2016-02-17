from django.template.loader import get_template
from django.http import HttpResponse
from blog.models import Post


def post(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except:
        return HttpResponse(status=404)

    template = get_template('blog/post.html')
    return HttpResponse(template.render({
        'p': post,
        'logged_in': request.user.is_authenticated(),
        'recent_posts': Post.objects.order_by('-created_at').all()[:10],
    }))


def home(request):
    template = get_template('blog/home.html')
    posts = Post.objects.order_by('-created_at').all()
    return HttpResponse(template.render({
        'posts': posts,
        'recent_posts': posts,
    }))


def search(request):
    template = get_template('blog/search.html')
    term = request.GET.get('search_term', '')
    posts = Post.objects.order_by('-created_at').filter(title__contains=term)
    return HttpResponse(template.render({
        'posts': posts,
        'recent_posts': posts,
        'term': term,
    }))
