from __future__ import with_statement
import re
import os
from fabric.api import settings, run, local, env
from fabric.contrib.console import confirm

APP_DIR = '/apps/my_django'
VIRTUAL_ENV = APP_DIR + '/env'

env.hosts = ['derekzeng.me']
env.user = 'coderek'
env.key = '/Users/derekzeng/.ssh/id_rsa.pub'
env.cwd = APP_DIR


def init_virtual_env():
    run('pip install virtualenv')
    if not os.path.exists(VIRTUAL_ENV):
        run('virtualenv {}'.format(VIRTUAL_ENV))


def pip_install():
    init_virtual_env()
    run('source {}'.format(os.path.join(VIRTUAL_ENV, 'bin', 'activate')))
    run('pip install -r {}/requirements.txt'.format(APP_DIR))


def git():
    run('git reset --hard origin/master')
    run('git pull')


def migrate():
    run('django_env=prod ./manage.py migrate')


def collectstatic():
    run('django_env=prod ./manage.py collectstatic --noinput -i node_modules')


def restart():
    run('supervisorctl -c /apps/my_django/supervisord.conf restart all')


def deploy():
    run('cd ' + APP_DIR)
    git()
    pip_install()
    migrate()
    collectstatic()
    restart()
