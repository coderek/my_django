from __future__ import absolute_import  # Python 2 only
from jinja2 import Environment


def environment(**options):
    env = Environment(**options)
    env.globals.update({
    })
    return env
