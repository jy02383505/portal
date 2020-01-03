import time
import json
import copy
import urllib
import requests
import random
import string
import hashlib
import datetime
from urllib import parse


class BaseAPI(object):
    def __init__(self, domain=''):
        self.domain = domain

    @staticmethod
    def link(url, method, headers, body=''):
        for i in range(3):
            try:
                response = None
                if method == 'POST':
                    response = requests.post(
                        url, data=body, headers=headers, timeout=60)
                elif method == 'GET':
                    response = requests.get(url, headers=headers, timeout=60)
                elif method == 'PUT':
                    response = requests.put(url, data=body, headers=headers,
                                            timeout=60)
                if response:
                    return response

            except Exception as e:
                print('请求超时，第%s次重复请求' % (i + 1), e)
                pass
        else:
            return -1


class ChinaCacheAPI(BaseAPI):
    """蓝汛相关api"""
    def __init__(self, protocol='http'):
        super().__init__()

        self.protocol = protocol

    @staticmethod
    def get_sign(content_type='application/json'):

        key = '3b195d9b8fef756c'
        secret = '9e0750615e8281287520da8fa70afcd0'

        timestamp = str(int(time.time()))
        nonce = "".join(random.sample(string.ascii_letters + string.digits, 10))

        str_list = [key, secret, timestamp, nonce]
        str_list_sorted = sorted(str_list)

        str_sorted = "".join(str_list_sorted).encode("utf-8")

        signature = hashlib.sha1(str_sorted).hexdigest()

        send_headers = {
            'X-CC-Auth-Key': key,
            'X-CC-Auth-Timestamp': timestamp,
            'X-CC-Auth-Nonce': nonce,
            'X-CC-Auth-Signature': signature
        }
        if content_type:
            send_headers["Content-Type"] = content_type

        return send_headers

    @classmethod
    def get_channel_by_cms(cls, cms_name='boyue'):
        """
        根据cms账号获取cms系统下该账号全部频道
        :param cms_name: cms ID
        :return:
        msft-novacdn
        """
        headers = cls.get_sign()

        url = (
            "http://openapi.chinacache.com/cloud-pbase/channels"
            "?cloud_curr_client_name={}"
        ).format(cms_name)

        method = 'GET'

        res = BaseAPI.link(url, method, headers)

        channel_list = []
        if res != -1:
            for i in res.json().get('data', []):
                channel_info = {
                    'channel_name': i.get('channel_name', ''),
                    'channel_id': i.get('channel_id', '')
                }
                channel_list.append(channel_info)

        return channel_list

    @classmethod
    def check_cert(cls, cms_name, domain, cert_name=''):
        """检查证书"""

        headers = cls.get_sign()

        url = (
            "http://openapi.chinacache.com/cloud-ca/config/certificates?"
            "cloud_curr_client_name={}"
        ).format(cms_name)

        if cert_name:
            params = {
                "cert_name": cert_name
            }
        else:
            params = {
                "channels": [
                    "https://%s" % domain
                ]
            }

        params = json.dumps(params)
        body = params.encode()

        print(body)

        method = 'POST'

        res = BaseAPI.link(url, method, headers, body=body)

        return res

    @staticmethod
    def get_contract_info(contract_num):
        """获取合同信息"""
        from urllib import request, parse

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

        sql = (
        "select Product__r.Name,Product__r.code__c,TopItem__r.OrderForm__"
        "r.begin__c,TopItem__r.OrderForm__r.end__c  from OrderItem__"
        "c where TopItem__r.OrderForm__r.ManualContractNumber__c='{}' "
        "and Product__r.NeedRCMSConfig__c=true".format(contract_num))
        sql_data = {'q': sql}
        # print(sql_data)

        sql_data = parse.urlencode(sql_data)

        temp_url = '/services/data/v37.0/query?'
        sql_url = '{}{}{}'.format(instance_url, temp_url, sql_data)
        sql_headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + access_token
        }

        method = 'GET'
        try:
            res = BaseAPI.link(sql_url, method, sql_headers)
            records = res.json().get('records', [])

            product_list = []
            for record in records:
                product_info = record.get('Product__r', {})
                product_dict = {
                    'product_name': product_info.get('Name', ''),
                    'product_code': product_info.get('code__c', '')
                }
                product_list.append(product_dict)
            else:
                time_info = record.get('TopItem__r', {}).get('OrderForm__r', {})
                start_time = time_info.get('begin__c', '')
                end_time = time_info.get('end__c', '')
        except Exception as e:
            print(e)
            start_time = ''
            end_time = ''
            product_list = []

        return start_time, end_time, product_list

    @staticmethod
    def get_cms_password(cms_username):
        """根据用户id获取用户apikey"""
        url = (
            'http://portal-api.chinacache.com/'
            'api/internal/getCustomer.do?username={}'
        ).format(cms_username)

        api_key = ''
        try:
            method = 'GET'

            headers = {
                'content-type': 'application/json'
            }

            res = BaseAPI.link(url, method, headers)
            res = res.json()
            api_key = res['apiPassword']
        except Exception as e:
            print('%s apiPassword get error' % cms_username, e)

        return api_key

if __name__ == '__main__':
    t = ChinaCacheAPI()
    a = t.get_cms_password('pasj')
    print(a)
