from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm

env.hosts = ['derekzeng.me']
env.user = 'root'
env.key = '/Users/derekzeng/.ssh/id_rsa.pub'

def test():
    run('ls')
