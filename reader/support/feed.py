import logging
from datetime import datetime
import feedparser
import pytz
from time import mktime, localtime
from reader.models import Feed, Entry


def fetch_feed(url):
    logging.warning('fetching feed from {}'.format(url))

    try:
        f = Feed.objects.get(feed_url=url)
        # use etag
        d = feedparser.parse(url, etag=f.etag)

        if d.status == 304:
            # nothing changed
            return f, None

    except Feed.DoesNotExist:
        d = feedparser.parse(url)

    try:
        feed = get_feed_obj(d)
        feed['feed_url'] = url

        f, created = Feed.objects.update_or_create(defaults=feed, feed_url=url)

        for entry_item in d['entries']:
            entry = get_entry_obj(entry_item)
            entry['feed'] = f
            logging.warning(entry['url'])
            Entry.objects.update_or_create(defaults=entry, uuid=entry['uuid'])

        return f, None
    except Exception as e:
        return None, e.message


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
    if 'content' in source:
        content = source.content[0].get('value')
    else:
        content = ''
    return {
        'title': source.title,
        'url': source.link,
        'author': source.author if 'author' in source else '',
        'summary': source.description,
        'content': content,
        'published': to_date_obj(published),
        'uuid': source.id if 'id' in source else source.title,
    }


def to_date_obj(time_parsed):
    return datetime.fromtimestamp(mktime(time_parsed)).replace(tzinfo=pytz.UTC)
