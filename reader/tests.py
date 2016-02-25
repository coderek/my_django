import json

from django.contrib.auth.models import User
from django.test import Client, TestCase

from reader.models import Entry, Feed
from reader.support.feed import fetch_feed


class TestFeed(TestCase):

    def test_fetch_feed(self):
        url = 'https://weworkremotely.com/categories/2/jobs.rss'
        f, error = fetch_feed(url)

        assert Feed.objects.count() == 0
        assert error

    def test_yc_feed(self):
        url = 'https://news.ycombinator.com/rss'
        f, error = fetch_feed(url)

        assert Feed.objects.count() == 1
        assert not error

    def test_chinese_feed(self):
        url = 'http://codingnow.com/atom.xml'

        fetch_feed(url)
        assert Feed.objects.count() == 1
        assert Entry.objects.count() > 0

    def test_coding_horror(self):
        url = 'http://blog.codinghorror.com/rss/'

        fetch_feed(url)
        assert Feed.objects.count() == 1
        assert Entry.objects.count() > 0

    def test_coolshell(self):
        url = 'http://coolshell.cn/feed'

        fetch_feed(url)
        assert Feed.objects.count() == 1
        assert Entry.objects.count() > 0

    def test_repeated(self):
        url = 'http://coolshell.cn/feed'

        fetch_feed(url)
        assert Feed.objects.count() == 1
        assert Entry.objects.count() > 0

        fetch_feed(url)
        assert Feed.objects.count() == 1

    def test_xdite(self):
        url = 'http://feeds.feedburner.com/xxddite'

        fetch_feed(url)
        assert Feed.objects.count() == 1
        assert Entry.objects.count() > 0

    def test_lucumr(self):
        url = 'http://lucumr.pocoo.org/feed.atom'

        fetch_feed(url)
        assert Feed.objects.count() == 1
        assert Entry.objects.count() > 0

    def test_techcrunch(self):
        url = 'http://techcrunch.cn/feed'

        fetch_feed(url)
        assert Feed.objects.count() == 1
        assert Entry.objects.count() > 0


class TestUpdateFeeds(TestCase):
    fixtures = ['feeds.yaml']

    def test_update_feed(self):
        assert Feed.objects.filter(pk=75).exists()


class TestAPI(TestCase):

    @classmethod
    def setUpClass(cls):
        User.objects.create_superuser('fred', 'fred@gmail.com', 'secret')

    def setUp(self):
        if not self.client:
            self.client = Client(
                # HTTP_X_REQUESTED_WITH='XMLHttpRequest',
                # HTTP_CONTENT_TYPE='application/json'
            )

    def test_get(self):
        # import pdb; pdb.set_trace()
        res = self.client.get(
            '/reader/api/feeds/', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        assert len(res.json()) == 0

    def test_post_forbidden(self):
        feed = {'url': 'https://weworkremotely.com/categories/2/jobs.rss'}
        res = self.client.post(
            '/reader/api/feeds/', feed, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        assert res.status_code == 403

    def test_post(self):
        assert self.client.login(username='fred', password='secret')
        feed = json.dumps({
            'url': 'https://weworkremotely.com/categories/2/jobs.rss'
        })
        res = self.client.post(
            '/reader/api/feeds/', feed,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
            content_type='application/json'
        )
        assert res.status_code == 200
        assert 'title' in res.json()
        assert 'id' in res.json()

    def test_delete(self):
        assert self.client.login(username='fred', password='secret')
        from reader.support.feed import fetch_feed
        f, err = fetch_feed('https://weworkremotely.com/categories/2/jobs.rss')
        assert not err

        res = self.client.delete(
            '/reader/api/feeds/{}'.format(f.id),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
            content_type='application/json'
        )
        assert not Feed.objects.filter(pk=f.id).exists()
        assert res.status_code == 200

    @classmethod
    def tearDownClass(cls):
        pass
