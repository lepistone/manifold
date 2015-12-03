# -*- coding: utf-8 -*-
import json
import os
import socket


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

    # Example: 'training/webapp'
    try:
        DOCKER_IMAGE = os.environ['DOCKER_IMAGE']
    except KeyError:
        raise Exception('DOCKER_IMAGE environment variable must be set')
    # Used to filter the containers, ('ps docker ps --filter')
    # It should be a json in the form expected by docker-py
    # https://docker-py.readthedocs.org/en/latest/api/#containers
    # Example:
    # '{"label": ["com.docker.compose.project=odoo",
    #             "com.docker.compose.service=odoo-xyz"]}'
    DOCKER_FILTER = json.loads(os.environ.get('DOCKER_FILTER') or '{}')

    def image_with_tag(self, tag):
        return '{}:{}'.format(ManifoldConfig.DOCKER_IMAGE, tag)
