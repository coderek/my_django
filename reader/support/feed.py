from datetime import datetime
import feedparser
import pytz
from time import mktime
from reader.models import Feed, Entry


def fetch_feed(url):
    try:
        f = Feed.objects.get(feed_url=url)
        # use etag
        d = feedparser.parse(url, etag=f.etag)

        if d.status == 304:
            # nothing changed
            return f

    except Feed.DoesNotExist:
        d = feedparser.parse(url)

    feed = get_feed_obj(d)
    feed['feed_url'] = url

    f, created = Feed.objects.update_or_create(defaults=feed, feed_url=url)

    for entry_item in d['entries']:
        entry = get_entry_obj(entry_item)
        entry['feed'] = f
        Entry.objects.update_or_create(defaults=entry, url=entry['url'])

    return f


def get_feed_obj(source):
    published_parsed = (
        source.feed.published_parsed
        if 'published_parsed' in source.feed else source.feed.updated_parsed
    )
    last_modified = to_date_obj(published_parsed)

    return {
        'title': source['channel']['title'],
        'description': source['channel']['description'],
        'etag': source.etag if 'etag' in source else '',
        'last_modified': last_modified,
    }


def get_entry_obj(source):
    published = to_date_obj(source.published_parsed)
    return {
        'title': source.title,
        'url': source.link,
        'author': source.author,
        'summary': source.description,
        'content': source.content[0].get('value'),
        'published': published,
        'uuid': source.id
    }


def to_date_obj(time_parsed):
    return datetime.fromtimestamp(mktime(time_parsed)).replace(tzinfo=pytz.UTC)
