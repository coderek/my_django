from __future__ import absolute_import  # Python 2 only

from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.urlresolvers import reverse

from jinja2 import Environment
from markupsafe import Markup


def static(raw_path):
    wrapper = '{}'
    # '{}{}'.format(settings.STATIC_URL, raw_path)
    path = staticfiles_storage.url(raw_path)
    if path.endswith('.scss'):
        wrapper = '<link rel="stylesheet" type="text/x-scss" href="{}">'
    if path.endswith('.css'):
        wrapper = '<link rel="stylesheet" type="text/css" href="{}">'
    if path.endswith('.js'):
        wrapper = '<script src="{}"></script>'
    return Markup(wrapper.format(path))


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'url': reverse,
        'static': static,
    })
    return env
