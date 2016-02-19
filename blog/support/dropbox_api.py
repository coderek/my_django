# -*- coding: utf-8-*-
import dropbox
import time
import contextlib
from blog.models import Post
from django.contrib.auth.models import User
from django.conf import settings

article_dir = '/文章'


def load_articles():
    dbx = dropbox.Dropbox(settings.DROPBOX_ACCESS_KEY)
    created_count = 0
    for entry in dbx.files_list_folder(article_dir).entries:
        data = download(dbx, entry.path_lower, entry.name)
        title = entry.name.split('.')[0]
        p, created = Post.objects.update_or_create(defaults={
            'title': title,
            'body': data,
            'author': User.objects.first(),
            'updated_at': entry.server_modified,
        }, title=title)
        created_count += int(created)
    return created_count


def download(dbx, path, name):
    """Download a file.
    Return the bytes of the file, or None if it doesn't exist.
    """
    with stopwatch('download'):
        try:
            md, res = dbx.files_download(path)
        except dropbox.exceptions.HttpError as err:
            print('*** HTTP error', err)
            return None
    data = res.content
    return data


@contextlib.contextmanager
def stopwatch(message):
    """Context manager to print how long a block of code took."""
    t0 = time.time()
    try:
        yield
    finally:
        t1 = time.time()
        print('Total elapsed time for %s: %.3f' % (message, t1 - t0))

