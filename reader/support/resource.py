import json

from django.http import (
    HttpResponse,
    HttpResponseForbidden,
    HttpResponseNotFound,
    JsonResponse,
    QueryDict,
)
from django.template.loader import get_template
from django.views.generic import View


class InvalidDataException(Exception):
    pass


class BaseView(View):
    model_cls = None
    template = None
    instance = None

    def parse_body(self, request):
        '''
        parse request body and set request.data based on content_type
        '''

        if request.method in ('GET', 'DELETE'):
            request.data = request.GET
        else:
            content_type = request.META.get('CONTENT_TYPE')

            try:
                # Because FF sends "application/json; charset=UTF-8"
                if content_type and 'application/json' in content_type:
                    request.data = json.loads(request.body)
                else:
                    # form data
                    request.data = QueryDict(request.body).copy()
            except:
                raise InvalidDataException

    @property
    def is_logged_in(self):
        return self.request.user.is_authenticated()

    def prepare(self, request, *args, **kwargs):
        pass

    def dispatch(self, request, *args, **kwargs):
        self.prepare(request, *args, **kwargs)
        self.parse_body(request)

        if 'pk' in kwargs:
            try:
                self.instance = self.model_cls.objects.get(pk=kwargs['pk'])
            except:
                return HttpResponseNotFound

        if request.is_ajax():
            if (request.method in ('POST', 'PUT', 'DELETE') and
                    not self.is_logged_in):
                return HttpResponseForbidden('Must login')
            # import pdb; pdb.set_trace()

            if request.method == 'GET':
                if self.instance:
                    return self.get(self.request)
                else:
                    return self.index(self.request)
            elif request.method == 'POST':
                return self.post(self.request, *args, **kwargs)
            elif request.method == 'PUT':
                return self.update(self.request, *args, **kwargs)
            elif request.method == 'DELETE':
                return self.delete(self.request, *args, **kwargs)
            else:
                self.http_method_not_allowed(self.request)
        else:
            return self.get(self.request)

    def get_context(self):
        return {
            'is_logged_in': self.request.user.is_authenticated()
        }

    def get(self, request):
        tpl = get_template(self.template)
        return HttpResponse(tpl.render(self.get_context()))


class CollectionAPI(BaseView):

    def index(self, request):
        all_models = self.model_cls.all()
        return JsonResponse(all_models, safe=False)

    def post(self, request):
        return JsonResponse(self.request.data)


class ModelAPI(BaseView):

    def get(self, request):
        pass

    def delete(self, request, pk):
        self.instance.delete()
        return JsonResponse({})

    def update(self, pk):
        pass
