import re
from datetime import datetime
import json
from django.core.management.base import BaseCommand
from django.conf import settings
from os import listdir, path
from blog.models import Post


POSTS_DIR = path.join(settings.BASE_DIR, 'blog', '_posts')
PREVIEW_SEPARATOR = '--preview--'

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for file in listdir(POSTS_DIR):
            if file.endswith('.md'):
                self._process_post(path.join(POSTS_DIR, file))

    def _process_post(self, post_path):
        preview = None
        body = None
        with open(post_path) as f:
            content = f.read()
            headers, content = self._detect_headers(content)

            splits = content.split(PREVIEW_SEPARATOR)
            if len(splits) > 1:
                preview, body = splits
            else:
                body = splits[0]

        post, created = Post.objects.update_or_create(
            id=headers.get('id'),
            defaults={
                'title': headers.get('title', 'no title ({})'.format(datetime.now())),
                'body': body,
                'preview': preview
            })

        with open(post_path, 'w') as f:
            f.write(json.dumps({
                'id': post.id,
                'title': post.title,
            }) + content)

    def _detect_headers(self, content):
        pattern = r'^({[^}{]+})'
        matchObject = re.match(pattern, content)

        if matchObject:
            pass
            headers = matchObject.group(1)
            try:
                headers = json.loads(headers)
            except:
                print 'parsing error'
                return {}, content
            else:
                return headers, content[matchObject.end(1):]
        else:
            return {}, content
