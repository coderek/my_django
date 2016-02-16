from django.test import TestCase
from reader.models import Feed, Entry
from reader.support.feed import fetch_feed


class TestFeed(TestCase):

    def test_fetch_feed(self):
        url = 'http://feeds.feedburner.com/codinghorror'
        fetch_feed(url)

        assert Feed.objects.count() == 1
        assert Entry.objects.count() > 0

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


class TestUpdateFeeds(TestCase):
    fixtures = ['feeds.yaml']

    def test_update_feed(self):
        assert Feed.objects.filter(pk=75).exists()
