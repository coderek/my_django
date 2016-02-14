from datetime import datetime
import feedparser
import pytz
from time import mktime
from reader.models import Feed, Entry


def fetch_feed(url):

    exist = Feed.objects.filter(feed_url=url).first()
    if exist:
        return (exist, 0)

    d = feedparser.parse(url)

    published_parsed = (
        d.feed.published_parsed
        if 'published_parsed' in d.feed else d.feed.updated_parsed
    )
    last_modified = datetime.fromtimestamp(mktime(published_parsed))
    last_modified = last_modified.replace(tzinfo=pytz.UTC)
    f = Feed.objects.create(
        title=d['channel']['title'],
        description=d['channel']['description'],
        etag=d.etag if 'etag' in d else '',
        last_modified=last_modified,
        feed_url=url,
    )

    for entry in d['items']:
        published = datetime.fromtimestamp(
            mktime(entry.published_parsed)).replace(tzinfo=pytz.UTC)

        Entry.objects.create(
            feed=f,
            title=entry.title,
            url=entry.link,
            author=entry.author,
            summary=entry.description,
            content=entry.content[0].get('value'),
            published=published,
            uuid=entry.id)

    return (f, 1)
