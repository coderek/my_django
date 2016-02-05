from datetime import datetime
import feedparser
import pytz
from time import mktime
from reader.models import Feed, Entry


def fetch_feed(url):
    d = feedparser.parse(url)
    channel = d.channel
    entries = d.entries

    last_modified = datetime.fromtimestamp(mktime(d.updated_parsed))
    last_modified = last_modified.replace(tzinfo=pytz.UTC)
    f = Feed.objects.create(
        title=channel.title,
        description=channel.description,
        etag=d.etag,
        last_modified=last_modified,
        feed_url=d.url)

    for entry in entries:
        published = datetime.fromtimestamp(
            mktime(entry.published_parsed)).replace(tzinfo=pytz.UTC)
        Entry.objects.create(
            feed=f,
            title=entry.title,
            url=entry.link,
            author=entry.author,
            summary=entry.summary,
            content=entry.content,
            published=published,
            uuid=entry.id)

    return f
