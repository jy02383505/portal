# -*- coding: utf-8 -*-

from .base import *


DEBUG = True
DEBUG_TOOLBAR_PATCH_SETTINGS = False


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '223.202.202.48',
        'PORT': '3306',
        'NAME': 'fuse_nova',
        'USER': 'rLukerUser',
        'PASSWORD': 'CsP_9r0up',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            },
    }
}

LOGIN_URL = '/base/customer_login/'

SSO_NAME = 'nova-test'

API_URL = "223.202.202.15:8800"

# API_URL = "127.0.0.1:8800"

# 本地测试可以用“*”，但是正式环境建议修改为指定域名
ALLOWED_HOSTS = [
    '*',
]