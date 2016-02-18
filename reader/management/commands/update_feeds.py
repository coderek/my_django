import logging
from django.core.management.base import BaseCommand
from reader.models import Feed
from reader.support.feed import fetch_feed

logger = logging.getLogger('django')


class Command(BaseCommand):
    def handle(self, *args, **options):
        for f in Feed.objects.all():
            try:
                fetch_feed(f.feed_url)
            except Exception as e:
                logger.error(e)
