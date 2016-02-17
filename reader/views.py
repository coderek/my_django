from django.template.loader import get_template
from django.http import HttpResponse


def home(request):
    tpl = get_template('reader/index.html')
    return HttpResponse(
        tpl.render({
            'is_logged_in': request.user.is_authenticated()
        }))
