import logging
import requests
from lxml.html.clean import Cleaner
import feedparser
import pytz

from datetime import datetime
from time import mktime, localtime
from reader.models import Feed, Entry

logger = logging.getLogger('django')


def fetch_feed(url):
    logger.warning('fetching feed from {}'.format(url))

    try:
        feed = Feed.objects.get(feed_url=url).as_dict()
    except Feed.DoesNotExist:
        feed = {'feed_url': url}

    r = requests.get(url, timeout=10)
    d = feedparser.parse(r.text)

    feed.update(get_feed_obj(d))

    f, created = Feed.objects.update_or_create(
        defaults=feed, feed_url=url)

    for _, entry_item in enumerate(d['entries']):
        try:
            entry = get_entry_obj(entry_item)
            entry['feed'] = f
            logger.warning(entry['url'])
            Entry.objects.update_or_create(
                defaults=entry, uuid=entry['uuid'])
        except:
            # just skip it
            pass

    return f


def get_feed_obj(source):
    f = source.feed
    published_parsed = (
        f.published_parsed
        if 'published_parsed' in f else (
            f.updated_parsed if 'updated_parsed' in f else localtime()
        )
    )
    last_modified = to_date_obj(published_parsed)

    return {
        'title': f.get('title'),
        'description': f.get('description'),
        'etag': source.get('etag', ''),
        'last_modified': last_modified,
    }


def get_entry_obj(source):
    published = (
        source.published_parsed
        if 'published_parsed' in source else (
            source.updated_parsed
            if 'updated_parsed' in source else localtime()
        )
    )
    try:
        content = source.content[0].get('value')
    except:
        content = '<p></p>'

    try:
        summary = source.description
    except:
        summary = '<p></p>'

    return {
        'title': source.title,
        'url': source.link,
        'author': source.author if 'author' in source else '',
        'summary': wash_html(summary),
        'content': wash_html(content),
        'published': to_date_obj(published),
        'uuid': source.id + '+' + source.link if 'id' in source else source.title,
    }


def to_date_obj(time_parsed):
    return datetime.fromtimestamp(mktime(time_parsed)).replace(tzinfo=pytz.UTC)


def wash_html(html):
    attrs = Cleaner.safe_attrs
    Cleaner.safe_attrs = attrs - frozenset(['width', 'height'])
    c = Cleaner()
    cleaned = c.clean_html(html)
    return cleaned


def do_fetch_all():
    for f in Feed.objects.all():
        try:
            fetch_feed(f.feed_url)
        except Exception as e:
            logger.error(e)
