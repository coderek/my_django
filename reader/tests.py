from django.test import TestCase
from reader.models import Feed, Entry
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

class TestUpdateFeeds(TestCase):
    fixtures = ['feeds.yaml']

    def test_update_feed(self):
        assert Feed.objects.filter(pk=75).exists()
