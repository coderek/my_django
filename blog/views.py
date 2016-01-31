from django.template.loader import get_template
from django.http import HttpResponse
from blog.models import Post


# Create your views here.
def default(request):
    template = get_template('posts.default.html')
    return HttpResponse(template.render(
        {'name': 'zengqiang '}
    ))


def home(request):
    template = get_template('blog/home.html')
    return HttpResponse(template.render({'posts': Post.objects.all()}))
