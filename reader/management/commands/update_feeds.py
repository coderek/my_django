import logging
from django.core.management.base import BaseCommand
from reader.support.feed import do_fetch_all

logger = logging.getLogger('django')


class Command(BaseCommand):
    def handle(self, *args, **options):
        do_fetch_all()
