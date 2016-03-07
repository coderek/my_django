import logging
import json

from django.test import Client, TestCase

from reader.models import Entry, Feed, Category
from reader.support.feed import fetch_feed, do_fetch_all

logger = logging.getLogger('django')


class FeedRelatedTests(TestCase):
    fixtures = ['categories.yaml', 'feeds.yaml']


class TestFeed(TestCase):
    fixtures = ['categories.yaml']

    def test_fetch_feed(self):
        url = 'https://weworkremotely.com/categories/2-programming/jobs.rss'
        fetch_feed(url)
        assert Category.objects.count() == 1
        assert Feed.objects.count() == 1

    def test_yc_feed(self):
        url = 'https://news.ycombinator.com/rss'
        f = fetch_feed(url)
        assert Feed.objects.count() == 1

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

    def test_terry(self):
        url = 'http://terrytai.me/rss.xml'
        fetch_feed(url)

        assert Feed.objects.count() == 1
        assert Entry.objects.count() == 10


class TestUpdateFeeds(FeedRelatedTests):
    def test_update_feed(self):
        do_fetch_all()
        assert Entry.objects.count() > 0


class TestAPI(TestCase):
    fixtures = ['categories.yaml', 'users.yaml']

    def setUp(self):
        if not self.client:
            self.client = Client(
                # HTTP_X_REQUESTED_WITH='XMLHttpRequest',
                # HTTP_CONTENT_TYPE='application/json'
            )

    def test_get(self):
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
            'url': 'https://weworkremotely.com/categories/2-programming/jobs.rss'
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
        assert Category.objects.count() == 1
        assert self.client.login(username='fred', password='secret')
        f = fetch_feed('https://weworkremotely.com/categories/2/jobs.rss')

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



class TestScrubber(TestCase):
    def test_wash_html(self):
        html = '''
        <img alt="messenger-spotify"
        class="attachment-post-thumbnail size-post-thumbnail wp-post-image"
        src="http://files.techcrunch.cn/2016/03/messenger-spotify.png?w=1024"
        style="float: left; margin: 0 10px 7px 0;"
        height="576"
        width="1024"></img>
        '''
        from reader.support.feed import wash_html
        import lxml
        result_html = wash_html(html)
        result_dom = lxml.html.fromstring(result_html)
        assert 'style' not in result_dom.attrib
        assert 'width' not in result_dom.attrib
        assert 'height' not in result_dom.attrib
