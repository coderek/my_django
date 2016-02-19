from django.test import TestCase
from blog.support.dropbox_api import load_articles


class TestDropboxAPI(TestCase):

    def test_connection(self):
        created_count = load_articles()
        assert created_count == 1
