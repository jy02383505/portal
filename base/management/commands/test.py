# -*- coding=utf-8 -*-
import json
import time
import requests
import datetime
import logging

from django.core.management.base import BaseCommand

from django.contrib.auth.models import Group, Permission
from base.functions import create_user
from base.models import GroupProfile, UserProfile, Domain
from common.feed import APIUrl
from cdn.ajax.base_ajax import get_domain_flux
from common.functions import get_this_month_time, datetime_to_timestamp

  
def foo():
    """获取刷新结果"""
    print(11111)
    body = {
        'start_time': 1570723200,
        # 'end_time': 1569858900,

        'end_time': 1570723200+3600,

        'domain_list': [
            'novatest06.ccindex.cn',
            'novalive01.ccindex.cn',
            'novalive02.ccindexnoicp.cn',
            'novalive03.ccindex.cn',
        ],
        'user_id': 27
    }
    api_res = APIUrl.post_link('cdn_domain_status_code_batch', body)

    print(api_res)

def foo1():

    with open('/home/xiangzheng/workspace/fusion_nova_portal/excel/cert_info', 'r') as f:
        cert_value = f.read()

    with open('/home/xiangzheng/workspace/fusion_nova_portal/excel/cert_key', 'r') as f:
        key_value = f.read()

    body = {
        'cert_name': 'xz_test_0009',
        'username': 'xz_test',
        'cert_value': cert_value,
        'key_value': key_value,
        # 'is_update': 1

    }
    api_res = APIUrl.post_link('ssl_cert_create_or_edit', body)

    print(api_res)

def foo2():

    body = {
        'cert_name': 'xz_test_0009',
        'user_id': 93,

    }
    api_res = APIUrl.post_link('ssl_cert_detail', body)

    print(api_res)

def foo3():
    start = time.time()
    user = UserProfile.objects.get(id=127)
    # domain_query = Domain.objects.filter(user=user)
    # domain_list = [d.domain for d in domain_query]

    domain_list = ['novatest06.ccindex.cn']

    start_time, end_time = get_this_month_time()

    start_time = datetime_to_timestamp(start_time)
    end_time = datetime_to_timestamp(end_time)

    _, sum_cdn_flux, _, max_cdn, _, _, _ = get_domain_flux(
        user.id, domain_list, start_time, end_time, [])

    print(sum_cdn_flux, max_cdn)
    print(time.time()-start)

def foo4():
    domain_list = ['clashofclanscdn.kunlun-cdn.com']
    user_id = 105
    start_time = 1567267200
    end_time = 1567267200 + 3600


    get_domain_flux(user_id, domain_list, start_time, end_time)

class Command(BaseCommand):

    def handle(self, *args, **options):
        foo()
