import json
import datetime

from urllib import request, parse

from django.core.management.base import BaseCommand

from base.models import *


def get_contract_info(contract_num):
    """获取合同信息"""
    username = 'api.read@chinacache.com'
    password = '1qaz2wsx'
    client_id = ('3MVG9ZL0ppGP5UrCa5UtBMboxnaMd80gmQNQa0uEFmo20'
                 'FAZlVjNW4mLNBxST_rgVSWuBWnxAtT8BzEoxE827')
    client_secret = '1947928722851296063'

    data = {
        'grant_type': 'password',
        'username': username,
        'password': password,
        'client_id': client_id,
        'client_secret': client_secret,
    }
    data = parse.urlencode(data).encode('utf-8')

    headers = {
        'content-type': 'application/x-www-form-urlencoded'
    }

    url = "https://login.salesforce.com/services/oauth2/token"
    req = request.Request(url, headers=headers, data=data)
    res = request.urlopen(req).read()
    res = res.decode('utf-8')
    res = json.loads(res)

    instance_url = res['instance_url']
    access_token = res['access_token']
    # sql = ("select code__c, Name, TopItem__r.OrderForm__r.begin__c, "
    #        "TopItem__r.OrderForm__r.end__c from OrderItem__c"
    #        " where ContractNumber__c = '{}'".format(contract_num))

    sql = ("select Product__r.Name,Product__r.code__c,TopItem__r.OrderForm__"
           "r.begin__c,TopItem__r.OrderForm__r.end__c  from OrderItem__"
           "c where TopItem__r.OrderForm__r.ManualContractNumber__c='{}' "
           "and Product__r.NeedRCMSConfig__c=true".format(contract_num))
    sql_data = {'q': sql}
    print(sql_data)

    sql_data = parse.urlencode(sql_data)

    temp_url = '/services/data/v37.0/query?'
    sql_url = '{}{}{}'.format(instance_url, temp_url, sql_data)
    sql_headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + access_token
    }
    sql_req = request.Request(sql_url, headers=sql_headers, method='GET')
    sql_res = request.urlopen(sql_req).read()
    sql_res = sql_res.decode('utf-8')
    sql_res = json.loads(sql_res)
    print(sql_res)

    """
    Product__r.Name,Product__r.code__c,TopItem__r.OrderForm__r.begin__c,TopItem__r.OrderForm__r.end__c 
    对应查询合同下可用的产品名称、产品的物料编码，合同开始时间，结束时间
    
    {
        'totalSize': 6,
        'done': True,
        'records': [{
            'attributes': {
                'type': 'OrderItem__c',
                'url': '/services/data/v37.0/sobjects/OrderItem__c/a1I0o00000fFaDlEAK'
            },
            'Product__r': {
                'attributes': {
                    'type': 'BUProduct__c',
                    'url': '/services/data/v37.0/sobjects/BUProduct__c/a0E0o00001djDwQEAU'
                },
                'Name': 'http视频点播加速服务',
                'code__c': '9010300000432'
            },
            'TopItem__r': {
                'attributes': {
                    'type': 'TopItem__c',
                    'url': '/services/data/v37.0/sobjects/TopItem__c/a1v0o00000CYng4AAD'
                },
                'OrderForm__r': {
                    'attributes': {
                        'type': 'OrderForm__c',
                        'url': '/services/data/v37.0/sobjects/OrderForm__c/a1H0o00000MGNe4EAH'
                    },
                    'begin__c': '2018-11-01',
                    'end__c': '2019-09-30'
                }
            }
        }, {
            'attributes': {
                'type': 'OrderItem__c',
                'url': '/services/data/v37.0/sobjects/OrderItem__c/a1I0o00000fFaDmEAK'
            },
            'Product__r': {
                'attributes': {
                    'type': 'BUProduct__c',
                    'url': '/services/data/v37.0/sobjects/BUProduct__c/a0E0o00001djEeDEAU'
                },
                'Name': 'Https视频点播加速',
                'code__c': '9100399900152'
            },
            'TopItem__r': {
                'attributes': {
                    'type': 'TopItem__c',
                    'url': '/services/data/v37.0/sobjects/TopItem__c/a1v0o00000CYng4AAD'
                },
                'OrderForm__r': {
                    'attributes': {
                        'type': 'OrderForm__c',
                        'url': '/services/data/v37.0/sobjects/OrderForm__c/a1H0o00000MGNe4EAH'
                    },
                    'begin__c': '2018-11-01',
                    'end__c': '2019-09-30'
                }
            }
        }, {
            'attributes': {
                'type': 'OrderItem__c',
                'url': '/services/data/v37.0/sobjects/OrderItem__c/a1I0o00000fFaEGEA0'
            },
            'Product__r': {
                'attributes': {
                    'type': 'BUProduct__c',
                    'url': '/services/data/v37.0/sobjects/BUProduct__c/a0E0o00001djDzeEAE'
                },
                'Name': '智能下载服务',
                'code__c': '9010400000164'
            },
            'TopItem__r': {
                'attributes': {
                    'type': 'TopItem__c',
                    'url': '/services/data/v37.0/sobjects/TopItem__c/a1v0o00000CYngOAAT'
                },
                'OrderForm__r': {
                    'attributes': {
                        'type': 'OrderForm__c',
                        'url': '/services/data/v37.0/sobjects/OrderForm__c/a1H0o00000MGNe4EAH'
                    },
                    'begin__c': '2018-11-01',
                    'end__c': '2019-09-30'
                }
            }
        }, {
            'attributes': {
                'type': 'OrderItem__c',
                'url': '/services/data/v37.0/sobjects/OrderItem__c/a1I0o00000fFaEHEA0'
            },
            'Product__r': {
                'attributes': {
                    'type': 'BUProduct__c',
                    'url': '/services/data/v37.0/sobjects/BUProduct__c/a0E0o00001djEbfEAE'
                },
                'Name': '智能下载服务-HTTPS',
                'code__c': '9100299900140'
            },
            'TopItem__r': {
                'attributes': {
                    'type': 'TopItem__c',
                    'url': '/services/data/v37.0/sobjects/TopItem__c/a1v0o00000CYngOAAT'
                },
                'OrderForm__r': {
                    'attributes': {
                        'type': 'OrderForm__c',
                        'url': '/services/data/v37.0/sobjects/OrderForm__c/a1H0o00000MGNe4EAH'
                    },
                    'begin__c': '2018-11-01',
                    'end__c': '2019-09-30'
                }
            }
        }, {
            'attributes': {
                'type': 'OrderItem__c',
                'url': '/services/data/v37.0/sobjects/OrderItem__c/a1I0o00000fFcpXEAS'
            },
            'Product__r': {
                'attributes': {
                    'type': 'BUProduct__c',
                    'url': '/services/data/v37.0/sobjects/BUProduct__c/a0E0o00001djDgyEAE'
                },
                'Name': 'HTTP静态网页加速服务',
                'code__c': '9010100000002'
            },
            'TopItem__r': {
                'attributes': {
                    'type': 'TopItem__c',
                    'url': '/services/data/v37.0/sobjects/TopItem__c/a1v0o00000CYpaSAAT'
                },
                'OrderForm__r': {
                    'attributes': {
                        'type': 'OrderForm__c',
                        'url': '/services/data/v37.0/sobjects/OrderForm__c/a1H0o00000MGNe4EAH'
                    },
                    'begin__c': '2018-11-01',
                    'end__c': '2019-09-30'
                }
            }
        }, {
            'attributes': {
                'type': 'OrderItem__c',
                'url': '/services/data/v37.0/sobjects/OrderItem__c/a1I0o00000fFcpYEAS'
            },
            'Product__r': {
                'attributes': {
                    'type': 'BUProduct__c',
                    'url': '/services/data/v37.0/sobjects/BUProduct__c/a0E0o00001djDgzEAE'
                },
                'Name': 'HTTPS静态网页加速服务',
                'code__c': '9010100000003'
            },
            'TopItem__r': {
                'attributes': {
                    'type': 'TopItem__c',
                    'url': '/services/data/v37.0/sobjects/TopItem__c/a1v0o00000CYpaSAAT'
                },
                'OrderForm__r': {
                    'attributes': {
                        'type': 'OrderForm__c',
                        'url': '/services/data/v37.0/sobjects/OrderForm__c/a1H0o00000MGNe4EAH'
                    },
                    'begin__c': '2018-11-01',
                    'end__c': '2019-09-30'
                }
            }
        }]
    }
    """
    contract_info = {}
    product_info = []
    begin_time = None
    end_time = None
    # # for name_info in sql_res['records']:
    # #     product_info.append((name_info['Name'], name_info['code__c']))
    # #     end_time = name_info['TopItem__r']['OrderForm__r']['end__c']
    # #     begin_time = name_info['TopItem__r']['OrderForm__r']['begin__c']
    # #     begin_time = datetime.datetime.strptime(begin_time, "%Y-%m-%d")
    # #     end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d")
    # #     end_time = end_time
    # #     begin_time = begin_time
    # # else:
    # #     product_info = list(set(product_info))
    # #     contract_info['product_info'] = product_info
    # #     contract_info['begin_time'] = begin_time
    # #     contract_info['end_time'] = end_time
    #
    # return contract_info


class Command(BaseCommand):

    def handle(self, *args, **options):
        contract = 'Microsoft-azure-1510（重录）-2'
        contract_info = get_contract_info(contract)
        print(contract_info)

