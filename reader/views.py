from django.template.loader import get_template
from django.http import HttpResponse


def home(request):
    tpl = get_template('reader/index.html')
    return HttpResponse(tpl.render())
