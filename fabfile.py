from __future__ import with_statement
import re
import os
from fabric.api import settings, run, local, env
from fabric.context_managers import prefix
from fabric.contrib.files import exists

APP_DIR = '/apps/my_django'
VIRTUAL_ENV = APP_DIR + '/env'

env.hosts = ['derekzeng.me']
env.user = 'coderek'
env.key = '/Users/derekzeng/.ssh/id_rsa.pub'
env.cwd = APP_DIR


def init_virtual_env():
    if not exists(VIRTUAL_ENV):
        run('pip install virtualenv')
        run('virtualenv {}'.format(VIRTUAL_ENV))
    else:
        print 'Virtual Env is already existed'


def pip_install():
    init_virtual_env()
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
    with prefix('source {}'.format(os.path.join(VIRTUAL_ENV, 'bin', 'activate'))):
        pip_install()
        migrate()
        collectstatic()
        restart()
