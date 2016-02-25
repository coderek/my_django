from reader.support.resource import CollectionAPI, BaseView


class HomeView(BaseView):
    template = 'reader/index.html'


class TestAPIClass(CollectionAPI):
    pass
