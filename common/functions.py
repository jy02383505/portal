from urllib import parse
import os
import re
import time
import json
import ldap3
import datetime
import requests
from binascii import a2b_hex
from Crypto.Cipher import AES

from django.conf import settings
from django.http import HttpResponse
from django.db.models import QuerySet

from common.feed import AccountsFeed as af
from base.models import UserProfile


PAGE_SIZE = 10    # 页面分页显示数据


def json_response(res):
    """返回结果json处理"""
    return HttpResponse(
        json.dumps(res, ensure_ascii=False),
        content_type='application/json; charset=utf-8')


def authorize(username, password):
    """ldap 校验"""
    ldap_host = "192.168.1.198"
    ldap_port = 389

    login_flag = False
    username = str(username)
    password = str(password)
    server = ldap3.Server(ldap_host, ldap_port, get_info=ldap3.ALL)
    conn = None
    try:
        assert len(username) > 4 and len(password) > 4
        user = 'chinacahce\\%s' % username
        conn = ldap3.Connection(
            server, user=user, password=password,
            auto_bind=True, authentication=ldap3.NTLM, receive_timeout=20)
        msg = conn.result
        conn.unbind()
        login_flag = True
        return login_flag, msg
    except Exception as e:
        if conn:
            conn.unbind()
        return login_flag, e


def sso_authorize(request, username, password):
    """chinacache sso 校验"""

    host = 'https://sso.chinacache.com/'
    client_name = 'nova-test'

    username = str(username)
    password = str(password)

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": "SIG=%s" % request.COOKIES.get('csrftoken'),
        "Host": "sso.chinacache.com",
        "Origin": "http://www.nova-test.com",
        "Referer": "http://www.nova-test.com:8888/base/login/",
    }

    body = {
        "username": username,
        "password": password,
        "clientName": client_name
    }

    requests.post(host, data=body, headers=headers)


def decrypt_to(word, key, vi):
    """解密"""
    BS = AES.block_size
    # pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
    # unpad = lambda s : s[0:-ord(s[-1])]
    try:
        mode = AES.MODE_CBC
        cipher = AES.new(key, mode, vi)
        decrypted = cipher.decrypt(a2b_hex(word)).decode()
    except Exception as e:
        print(1111111, word, key, vi)
        print(e)
        decrypted = ''

    return decrypted


def int_check(p):
    """
    整型参数校验
    :param p: 校验的数值
    :return: None or int(p)
    """
    res = None

    try:
        res = int(p)
    except ValueError:
        pass

    return res


def float_check(p):
    """
    整型参数校验
    :param p: 校验的数值
    :return: None or int(p)
    """
    res = None

    try:
        res = float(p)
    except ValueError:
        pass

    return res


def get_pagination(current_page, count, page_limit):
    """分页"""
    try:
        page_list = []
        if count % page_limit == 0:
            page_count = count / page_limit
        else:
            page_count = int(count / page_limit)+1
        if page_count <= 5:
            start_num = 1
            end_num = page_count+1
        else:
            if current_page+3 > page_count:
                start_num = page_count-4
                end_num = page_count+1
            elif current_page-3 < 1:
                start_num = 1
                end_num = 6
            else:
                start_num = current_page - 2
                end_num = current_page + 3
        for i in range(int(start_num), int(end_num)):
            page_list.append(i)
        return {'page_count': page_count,
                'page_nums': page_list, 'total': count}
    except Exception as e:
        print(e)
        return {'page_count': 0, 'page_nums': 0, 'total': 0}


def data_pagination(request, data_list):
    """数据分页处理"""
    msg = ''
    size = request.POST.get('size', PAGE_SIZE)
    page = request.POST.get('page', '1')

    pagination = None
    try:
        size = int_check(size)
        page = int_check(page)
        if size is None or page is None or page == 0:
            msg = af.PARAME_ERROR
            assert False

        start = (page - 1) * size
        end = page * size

        if isinstance(data_list, QuerySet):
            total = data_list.count()
        elif isinstance(data_list, list):
            total = len(data_list)
        pagination = get_pagination(page, total, size)

        result_list = data_list[start:end]
    except AssertionError:
        result_list = []

    return msg, result_list, pagination


def str_to_datetime(time_str, _format='%Y-%m-%d %H:%M:%S'):
    """
    :param time_str: 2016-01-01 00：00：00
    :param _format: 时间格式 %Y-%m-%d %H:%M:%S
    :return: datetime.datetime(2016, 1, 1, 0, 0, 0)
    """
    temp_time = time.strptime(time_str, _format)
    result_datetime = datetime.datetime(*temp_time[:6])
    return result_datetime


def datetime_to_str(date_time, _format='%Y-%m-%d %H:%M:%S'):
    """
    :param date_time: datetime.datetime(2016, 1, 1, 0, 0, 0)
    :param _format: 时间格式 %Y-%m-%d %H:%M:%S
    :return: 2016-01-01 00：00：00
    """
    return date_time.strftime(_format)


def datetime_to_timestamp(date_time):
    """
    :param date_time: datetime.datetime(2016, 1, 1, 0, 0, 0)
    :return: 1451577600
    """
    return int(time.mktime(date_time.timetuple()))


def timestamp_to_datetime(timestamp):
    """
    :param timestamp: 1451577600
    :return: datetime.datetime(2016, 1, 1, 0, 0, 0)
    """
    return datetime.datetime.fromtimestamp(timestamp)


def timestamp_to_str(timestamp, _format='%Y-%m-%d %H:%M:%S'):
    """
    :param timestamp: 1451577600
    :param _format: 时间格式 %Y-%m-%d %H:%M:%S
    :return: 2016-01-01 00：00：00
    """
    return time.strftime(_format, time.localtime(timestamp))


def str_to_timestamp(time_str, _format='%Y-%m-%d %H:%M:%S'):
    """
    :param time_str: 2016-01-01 00：00：00
    :param _format: 时间格式 %Y-%m-%d %H:%M:%S
    :return: 1451577600
    """
    return int(time.mktime(time.strptime(time_str, _format)))


def datetime_correction(_datetime, fix=5):
    """
    时间修正
    :param _datetime: 需要修正的时间datetime.datetime(2016, 1, 1, 0, 4, 0)
    :param fix: 修正系数
    :return: datetime.datetime(2016, 1, 1, 0, 0, 0)
    """
    is_timestamp = False
    if isinstance(_datetime, int):
        is_timestamp = True
        _datetime = timestamp_to_datetime(_datetime)

    target_time = datetime.datetime(_datetime.year, _datetime.month,
                                    _datetime.day, _datetime.hour,
                                    _datetime.minute)

    if (target_time.minute % fix) != 0:
        sub = target_time.minute % fix
        target_time -= datetime.timedelta(minutes=sub)

    if is_timestamp:
        target_time = datetime_to_timestamp(target_time)

    return target_time


def file_iterator(file_name, chunk_size=512):
    """文件迭代"""
    try:
        with open(file_name, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    os.remove(file_name)
                    break
    except Exception as e:
        print("文件迭代错误:" + str(e))


def is_domain(domain, is_extensive=False):
    """校验域名"""
    if (' ' in domain) or (' ' in domain):
        return False
    if is_extensive and domain.startswith('*.'):
        domain = domain[2:]
    if domain.endswith('.'):
        domain = domain[:-1]
    domain_pattern = re.compile('^[0-9a-zA-Z]+[0-9a-zA-Z\.-]*\.[a-zA-Z]{2,10}$')
    if domain_pattern.search(domain):
        return True
    else:
        return False


def is_private_ip(ip):
    """判断内部ip"""
    if not is_ip(ip):
        return False
    if ip.startswith('192.168.') or ip.startswith('10.') \
            or ip.startswith('127.'):
        return True
    l = ip.split('.')
    if l[0] == '172' and 16 <= int(l[1]) <= 31:
        return True
    return False


def is_ip(ip, is_inner=False):
    """判断ip格式"""
    pip = re.compile(
        '^((25[0-5])|(2[0-4]\d)|(1\d\d)|([1-9]\d)|\d)'
        '(\.((25[0-5])|(2[0-4]\d)|(1\d\d)|([1-9]\d)|\d)){3}$')
    if pip.search(ip):
        if is_inner:
            if is_private_ip(ip):
                return False
        return True
    else:
        return False


def make_error_file(file_name, msg):
    """生成错误文件"""

    # 判断目录是否存在,不存在则创建新目录
    cwd = os.path.join(settings.BASE_DIR, 'excel')
    if not os.path.exists(cwd):
        os.makedirs(cwd)

    # 判断文件是否存在,存在则删除
    file_path = os.path.join(cwd, file_name)
    if os.path.exists(file_path):
        os.remove(file_path)

    with open(file_path, 'w') as f:
        f.write(msg)

    return file_path


def get_this_month_time():
    """获取本月时间"""

    now = datetime.datetime.now()
    start_time = datetime.datetime(now.year, now.month, 1, 0, 0)
    end_time = datetime_correction(now)

    return start_time, end_time


def handle_list(req_list, dec_int=False):
    """处理页面json 列表"""

    try:
        req_list = json.loads(req_list)
    except Exception as e:
        print(e)
        req_list = []
    result_list = []
    for i in req_list:

        if dec_int:
            i = int_check(i)

        if i != '' and not i is None:
            result_list.append(i)


    return result_list


def handle_request_user(request):
    """处理请求中的user"""
    try:
        if 'user_id' in request.POST:
            user_id = request.POST.get('user_id', '')

            user_id = int_check(user_id)
            if user_id is None:
                assert False

            user = UserProfile.objects.filter(id=user_id).first()
            if not user:
                assert False

        elif 'username' in request.POST:
            username = request.POST.get('username', '')
            user = UserProfile.objects.filter(username=username).first()
            if not user:
                assert False
        else:
            user = None

    except AssertionError:
        user = None

    return user


def handle_req_time(start_time, end_time):
    """处理请求中的时间"""
    msg = ''
    try:
        start_time = int_check(start_time)
        if start_time is None:
            msg = af.PARAME_ERROR
            assert False
        start_time = datetime_correction(start_time)

        end_time = int_check(end_time)
        if end_time is None:
            msg = af.PARAME_ERROR
            assert False
        end_time = datetime_correction(end_time)
    except AssertionError:
        pass

    return msg, start_time, end_time


def parseProtocolRecordDomain(channel):
    if not channel.startswith('http'):
        return None, None, None

    channelProtocol = 'https' if channel.startswith('https') else 'http'
    netloc = parse.urlparse(channel).netloc
    netlocArr = netloc.split('.')
    length = len(netlocArr)
    if length < 3:
        return channelProtocol, '', netloc
    return channelProtocol, netlocArr[0], '.'.join(netlocArr[1:])