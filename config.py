# -*- coding: utf-8 -*-
import os
import socket


repo = 'training/webapp'
tag = 'latest'
# repo = 'lepistone/test-subject'
# tag = 'master'

image = '{}:{}'.format(repo, tag)


class FlaskConfig(object):
    SECRET_KEY = os.environ.get('SECRET_KEY', '')
    DEBUG = os.environ.get('DEBUG', False)


class ManifoldConfig(object):
    NGINX_CONF_PATH = os.environ.get('NGINX_CONF_PATH',
                                     '/etc/nginx/conf.d/default.conf')
    NGINX_PASSWD_PATH = os.environ.get('NGINX_PASSWD_PATH')
    NGINX_CONTAINER = os.environ.get('NGINX_CONTAINER', 'manifoldoo_nginx_1')
    SUBDOMAIN = os.environ.get('SUBDOMAIN', 'manifold')
    DOMAIN = os.environ.get('DOMAIN', socket.gethostname())
