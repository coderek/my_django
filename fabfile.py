from __future__ import with_statement
import re
import os
from fabric.api import settings, run, local, env
from fabric.contrib.console import confirm

APP_DIR = '/apps/my_django'
VIRTUAL_ENV = APP_DIR + '/env'

env.hosts = ['derekzeng.me']
env.user = 'root'
env.key = '/Users/derekzeng/.ssh/id_rsa.pub'
env.cwd = APP_DIR


def init_virtual_env():
    run('pip install virtualenv')
    if not os.path.exists(VIRTUAL_ENV):
        run('virtualenv {}'.format(VIRTUAL_ENV))


def pip_install():
    init_virtual_env()
    run('pip install -r {}/requirements.txt'.format(APP_DIR))
    run('source {}'.format(os.path.join(VIRTUAL_ENV, 'bin', 'activate')))


def git():
    run('git reset --hard origin/master')
    run('git pull')


def migrate():
    run('django_env=prod ./manage.py migrate')


def collectstatic():
    run('django_env=prod ./manage.py collectstatic --noinput -i node_modules')


def restart():
    output = run('ps aux | grep "gunicorn: master" | grep my_django.wsgi')
    l = output.split('\n')[0]
    pid = re.split(r'\s+', l)[1]
    try:
        run('kill -TERM {}'.format(pid))
    except:
        pass
    run('django_env=prod gunicorn my_django.wsgi')


def deploy():
    run('cd ' + APP_DIR)
    git()
    pip_install()
    migrate()
    collectstatic()
