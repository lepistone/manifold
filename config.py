# -*- coding: utf-8 -*-
import os


repo = 'postgres'
tag = 'latest'
# repo = 'lepistone/test-subject'
# tag = 'master'

image = '{}:{}'.format(repo, tag)


class FlaskConfig(object):
    SECRET_KEY = os.environ.get('SECRET_KEY', '')
    DEBUG = os.environ.get('DEBUG', False)
