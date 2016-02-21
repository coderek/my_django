#!/bin/bash
source /root/django/bin/activate && /root/my_django/manage.py update_feeds >> /var/log/django/debug.log 2>&1
