# coding=utf-8

import copy
import json
from urllib.parse import urlparse

from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required


from common.decorators import rights_required
from common.fusion_api.cc_api import ChinaCacheAPI
from common.feed import AccountsFeed as af, OperateMsg as om, APIUrl, CDNConf
from common.functions import (json_response, int_check, data_pagination,
                              handle_list, handle_req_time)
from cdn.funcions import detect_domain

from base.models import Domain, UserProfile, Product, OperateLog



def get_domain_flux(user_id, domain_list, start_time, end_time, opts):
    """获取域名计费&回源数据"""

    body = {
        'domain_list': domain_list,
        'user_id': user_id,
        'start_time': start_time,
        'end_time': end_time,
        'opts': opts,
        'sep': True
    }

    print(body)

    sum_cdn_flux = 0    # 总计费数据（MB）
    sum_src_flux = 0    # 总回源数据（MB）
    max_cdn = 0    # 峰值计费值(Mbps)
    max_src = 0  # 峰值回源值(Mbps)

    all_flux_list = []

    table_data = []    # 每日数据

    opt_result = {}

    try:
        api_res = APIUrl.post_link('cdn_domain_flux_batch', body)

        return_code = api_res.get('return_code')
        if return_code != 0:
            assert False

        result = api_res.get('result', {})

        table_temp_data = {}

        all_flux = {}

        opt_flux = {}

        for opt in result:

            opt_flux.setdefault(opt, {})

            for data in result[opt]:

                time_key = data['time_key']
                cdn_data = data['cdn_data']
                src_data = data['src_data']

                all_flux.setdefault(time_key, [0, 0])
                all_flux[time_key][0] += cdn_data
                all_flux[time_key][1] += src_data

                opt_flux[opt].setdefault(time_key, [0, 0])
                opt_flux[opt][time_key][0] += cdn_data
                opt_flux[opt][time_key][1] += src_data

                sum_cdn_flux += cdn_data
                sum_src_flux += src_data

        for time_key in all_flux:

            cdn_data = all_flux[time_key][0] / 300 * 8
            src_data = all_flux[time_key][1] / 300 * 8

            if cdn_data >= max_cdn:
                max_cdn = cdn_data

            if src_data >= max_src:
                max_src = src_data

            flux_dict = {
                'time_key': time_key,
                'cdn_data': cdn_data,
                'src_data': src_data,
            }
            all_flux_list.append(flux_dict)

            day_key = time_key[:10]
            table_temp_data.setdefault(day_key, [])
            table_temp_data[day_key].append(flux_dict)

        max_cdn = max_cdn
        max_src = max_src

        all_flux_list = sorted(all_flux_list, key=lambda x: x['time_key'])

        for opt in opt_flux:

            temp_list = []
            for time_key in opt_flux[opt]:
                flux_dict = {
                    'time_key': time_key,
                    'cdn_data': all_flux[time_key][0],
                    'src_data': all_flux[time_key][1],
                }
                temp_list.append(flux_dict)

            temp_list = sorted(temp_list, key=lambda x: x['time_key'])

            opt_result[opt] = temp_list

        # 按天切割数据
        for day in table_temp_data:
            day_cdn_flux = 0
            day_src_flux = 0
            day_max_cdn = 0
            day_max_cdn_time = ''
            day_max_src = 0
            day_max_src_time = ''

            for i in table_temp_data[day]:

                day_cdn_flux += i['cdn_data'] * 300 / 8
                day_src_flux += i['src_data'] * 300 / 8

                if i['cdn_data'] >= day_max_cdn:
                    day_max_cdn = i['cdn_data']
                    day_max_cdn_time = i['time_key']

                if i['src_data'] >= day_max_src:
                    day_max_src = i['src_data']
                    day_max_src_time = i['time_key']

            day_info = {
                'day_cdn_flux': day_cdn_flux,
                'day_src_flux': day_src_flux,
                'day_max_cdn': day_max_cdn,
                'day_max_cdn_time': day_max_cdn_time,
                'day_max_src': day_max_src,
                'day_max_src_time': day_max_src_time,
                'day': day,
            }
            table_data.append(day_info)

        table_data = sorted(table_data, key=lambda x: x['day'])

    except AssertionError:
        pass

    return (all_flux_list, sum_cdn_flux, sum_src_flux,
            max_cdn, max_src, table_data, opt_result)


def get_domain_request(user_id, domain_list, start_time, end_time, opts):
    """获取域名计费&回源数据"""

    body = {
        'domain_list': domain_list,
        'user_id': user_id,
        'start_time': start_time,
        'end_time': end_time,
        'opts': opts,
        'sep': True
    }


    ratio = 0
    try:
        api_res = APIUrl.post_link('cdn_domain_request', body)

        return_code = api_res.get('return_code')
        if return_code != 0:
            assert False

        result = api_res.get('result', {})

        sum_req = 0
        sum_hit = 0
        for domain in result:
            for opt in result[domain]:
                for data in result[domain][opt]:
                    sum_req += data['requests']
                    sum_hit += data['hit']

        else:
            if sum_hit and sum_req:
                ratio = sum_hit / sum_req
                ratio = round(ratio, 4) * 100
    except AssertionError:
        pass

    return ratio


def get_domain_status_code(user_id, domain_list, start_time, end_time, opts):
    """获取域名计费&回源数据"""

    body = {
        'domain_list': domain_list,
        'user_id': user_id,
        'start_time': start_time,
        'end_time': end_time,
        'sep': True,
        'opts': opts,
    }


    all_status_code = {}
    opt_status_code = {}

    all_trend_data = {}
    opt_trend_data = {}

    all_trend_result = []

    try:
        print(body)
        api_res = APIUrl.post_link('cdn_domain_status_code', body)
        # print(api_res)

        return_code = api_res.get('return_code')
        if return_code != 0:
            assert False

        result = api_res.get('result', {})

        for domain in result:
            for opt in result[domain]:
                opt_status_code.setdefault(opt, {})

                for data in result[domain][opt]:

                    for k in data:
                        if k != 'time_key':
                            all_status_code.setdefault(k, 0)
                            all_status_code[k] += data.get(k, 0)

                            opt_status_code[opt].setdefault(k, 0)
                            opt_status_code[opt][k] += data.get(k, 0)

        trend_result = api_res.get('trend_result', {})

        status_code_trend = {}
        for domain in trend_result:
            for opt in trend_result[domain]:

                opt_trend_data.setdefault(opt, {})

                for code_info in trend_result[domain][opt]:

                    for code in code_info:

                        time_key = code_info['time_key']

                        status_code_trend.setdefault(time_key, {})

                        if code != 'time_key':
                            status_code_trend[time_key].setdefault(code, 0)
                            status_code_trend[time_key][code] += code_info[code]

                            all_trend_data.setdefault(code, 0)
                            all_trend_data[code] += code_info[code]

                            opt_trend_data[opt].setdefault(code, 0)
                            opt_trend_data[opt][code] += code_info[code]

        for time_key in status_code_trend:
            code_dict = copy.deepcopy(status_code_trend[time_key])
            code_dict['time_key'] = time_key
            all_trend_result.append(code_dict)

        all_trend_result = sorted(all_trend_result, key=lambda x: x['time_key'])

    except AssertionError:
        pass

    return (all_status_code, opt_status_code, all_trend_result,
            all_trend_data, opt_trend_data)


def get_domain_list(request, domain_query, cdn_type, domain_status):
    """获取域名列表"""

    check_domain = []
    channel_list = []
    domain_obj_list = []
    for i in domain_query:
        domain = i.domain
        if domain not in check_domain:
            check_domain.append(domain)
            channel_list.append(i.channel)
            domain_obj_list.append(i)

    body = {
        'channel_list': channel_list,
        'cdn_type': cdn_type,
        'domain_status': domain_status
    }

    api_res = APIUrl.post_link('cdn_domain_query', body)

    api_domain_query = api_res.get('domain_query', {})

    domain_dict_list = []

    domain_dict_query = {}
    for i in domain_obj_list:
        domain = i.domain
        channel = i.channel

        api_domain_info = api_domain_query.get(channel, {})

        if not api_domain_info:
            continue

        if 'modify_time' in api_domain_info:
            api_domain_info.pop('modify_time')
        if 'task_id' in api_domain_info:
            api_domain_info.pop('task_id')
        if 'channel_id' in api_domain_info:
            api_domain_info.pop('channel_id')
        if 'dis_cname' in api_domain_info:
            api_domain_info.pop('dis_cname')
        if 'channel' in api_domain_info:
            api_domain_info.pop('channel')

        cdn_type = CDNConf.get_cdn_type_name(api_domain_info['cdn_type'])
        status = CDNConf.get_status_name(api_domain_info['status'])

        api_domain_info['cdn_type'] = cdn_type
        api_domain_info['status'] = status
        api_domain_info['id'] = i.id
        api_domain_info['username'] = i.user.username
        api_domain_info['user_id'] = i.user.id

        if domain not in domain_dict_query:
            domain_dict_query[domain] = api_domain_info
        else:
            old_progress = domain_dict_query[domain]['task_progress']
            now_progress = api_domain_info['task_progress']

            if now_progress < old_progress:
                domain_dict_query[domain] = api_domain_info

    for i in domain_dict_query:
        domain_dict_list.append(domain_dict_query[i])

    domain_dict_list = sorted(
        domain_dict_list, key=lambda x: x['id'], reverse=True)

    check_msg, domain_dict_list, pagination = data_pagination(
        request, domain_dict_list)

    return check_msg, domain_dict_list, pagination


def user_domain_refresh(request, user):
    """用户刷新"""

    print(request.POST)
    urls = request.POST.get('urls', '[]')
    dirs = request.POST.get('dirs', '[]')

    user_id = user.id

    body = {
        'user_id': user_id,
    }

    msg = ''

    try:
        urls = handle_list(urls)
        if urls:
            urls = detect_domain(user_id, urls)
            if not urls:
                msg = af.URL_FORMAT_ERROR
                assert False

            body['urls'] = urls

        dirs = handle_list(dirs)
        if dirs:
            dirs = detect_domain(user_id, dirs)
            if not dirs:
                msg = af.URL_FORMAT_ERROR
                assert False

            body['dirs'] = dirs

        api_res = APIUrl.post_link('cdn_domain_refresh', body)
        return_code = api_res.get('return_code', 0)

        if return_code != 0:
            msg = af.SEND_ERROR
            assert False
    except AssertionError:
        pass

    return msg


def user_domain_refresh_status(request, user):
    """用户刷新查询"""

    start_time = request.POST.get('start_time', 0)
    end_time = request.POST.get('end_time', 0)
    url = request.POST.get('url', '')
    refresh_type = request.POST.get('refresh_type', '')
    refresh_status = request.POST.get('refresh_status', '')

    msg = ''
    result_list = []
    pagination = {}
    try:
        start_time = int_check(start_time)
        if start_time is None:
            msg = af.PARAME_ERROR
            assert False

        end_time = int_check(end_time)
        if end_time is None:
            msg = af.PARAME_ERROR
            assert False

        body = {
            'username': user.username,
            'start_time': start_time,
            'end_time': end_time,
            'url': url,
            'type': refresh_type,
            'status': refresh_status,

        }
        api_res = APIUrl.post_link('cdn_domain_refresh_status', body)
        return_code = api_res.get('return_code', 0)

        if return_code != 0:
            assert False

        result_list = api_res.get('result_list', [])

        check_msg, result_list, pagination = data_pagination(
            request, result_list)

        if check_msg:
            msg = check_msg
            assert False

    except AssertionError:
        pass

    return msg, result_list, pagination


def user_domain_preload(request, user):
    """用户刷新"""

    urls = request.POST.get('urls', '[]')

    user_id = user.id

    msg = ''

    try:
        urls = handle_list(urls)
        if urls:
            urls = detect_domain(user_id, urls)
            if not urls:
                msg = af.URL_FORMAT_ERROR
                assert False

        body = {
            'user_id': user.id,
            'urls': urls,
        }
        print(body)
        api_res = APIUrl.post_link('cdn_domain_preload', body)
        print(api_res)
        return_code = api_res.get('return_code', 0)

        if return_code != 0:
            msg = af.SEND_ERROR
            assert False

    except AssertionError:
        pass

    return msg


def user_domain_preload_status(request, user):
    """预热查询"""
    start_time = request.POST.get('start_time', 0)
    end_time = request.POST.get('end_time', 0)
    url = request.POST.get('url', '')
    preload_status = request.POST.get('preload_status', '')

    msg = ''
    result_list = []
    pagination = {}
    try:
        start_time = int_check(start_time)
        if start_time is None:
            msg = af.PARAME_ERROR
            assert False

        end_time = int_check(end_time)
        if end_time is None:
            msg = af.PARAME_ERROR
            assert False

        body = {
            'username': user.username,
            'start_time': start_time,
            'end_time': end_time,
            'url': url,
            'status': preload_status,

        }
        print(body)
        api_res = APIUrl.post_link('cdn_domain_preload_status', body)
        # print(api_res)

        return_code = api_res.get('return_code', 0)
        if return_code != 0:
            assert False

        result_list = api_res.get('result_list', [])

        check_msg, result_list, pagination = data_pagination(
            request, result_list)

        if check_msg:
            msg = check_msg
            assert False

    except AssertionError:
        pass

    return msg, result_list, pagination


def get_domain_conf(domain_obj, provider='CC'):
    """获取域名配置"""

    body = {
        'user_id': domain_obj.user.id,
        'protocol': domain_obj.protocol,
        'domain': domain_obj.domain,
        'provider': provider
    }

    try:
        api_res = APIUrl.post_link('cdn_domain_sync_conf', body)
        return_code = api_res.get('return_code', 0)

        if return_code != 0:
            assert False

        assert 'domain_conf' in api_res
        domain_conf = api_res['domain_conf']

        domain_obj.create_time = domain_conf.get('create_time', '')
        domain_obj.cname = domain_conf.get('cname', '')

        domain_cdn_type = ''
        cdn_type = domain_conf.get('cdn_type', '')
        for i in CDNConf.CDN_TYPE:
            if cdn_type == i['check_name']:
                domain_cdn_type = i['name']
                break
        domain_obj.cdn_type = domain_cdn_type

        domain_status = ''
        status = domain_conf.get('status', '')
        for i in CDNConf.DOMAIN_STATUS:
            if status in i['id']:
                domain_status = i['name']
                break
        domain_obj.status = domain_status

        domain_src_type = ''
        src_value = ''
        src_type = domain_conf.get('src_type', '')
        for i in CDNConf.SRC_TYPE:
            if src_type == i['id']:
                domain_src_type = i['name']

                if src_type == CDNConf.SRC_IP:
                    src_ips = domain_conf.get('src_ips', '')
                    src_value = ';'.join(src_ips)
                elif src_type == CDNConf.SRC_DOMAIN:
                    src_value = domain_conf.get('src_domain', '')
                break
        domain_obj.src_type = domain_src_type
        domain_obj.src_value = src_value

        domain_src_back_type = ''
        src_back_value = ''
        src_back_type = domain_conf.get('src_back_type', '')
        for i in CDNConf.SRC_BACK_TYPE:
            if src_back_type == i['id']:
                domain_src_back_type = i['name']

                if src_back_type == CDNConf.SRC_BACK_IP:
                    src_back_ips = domain_conf.get('src_back_ips', '')
                    src_back_value = ';'.join(src_back_ips)
                elif src_back_type == CDNConf.SRC_BACK_DOMAIN:
                    src_back_value = domain_conf.get('src_back_domain', '')
                break
        domain_obj.src_back_type = domain_src_back_type
        domain_obj.src_back_value = src_back_value

        domain_obj.src_host = domain_conf.get('src_host', '')

        domain_obj.cache_rule = domain_conf.get('cache_rule', {})

        domain_obj.ignore_query_string = domain_conf.get(
            'ignore_query_string', 0)

        domain_obj.ignore_cache_control = domain_conf.get(
            'ignore_cache_control', 0)

        print(domain_obj.ignore_query_string, domain_obj.ignore_cache_control)

        domain_obj.cert_info = domain_conf.get('cert_info', {})
    except AssertionError:
        pass

    return domain_obj


def user_domain_create(request, user, opt_user):
    """用户创建域名"""

    domain = request.POST.get('domain', '')

    contract_name = request.POST.get('contract_name', '')
    cdn_type = request.POST.get('cdn_type', '')

    protocol = request.POST.get('protocol', '[]')
    cert_name = request.POST.get('cert_name', '')
    src_type = request.POST.get('src_type', '')
    src_value = request.POST.get('src_value', '')
    src_host = request.POST.get('src_host', '')

    src_back_type = request.POST.get('src_back_type', '')
    src_back_value = request.POST.get('src_back_value', '')

    ignore_cache_control = request.POST.get('ignore_cache_control', '0')
    ignore_query_string = request.POST.get('ignore_query_string', '0')

    cache_rule = request.POST.get('cache_rule', '[]')

    msg = ''
    status = False

    try:
        protocol = handle_list(protocol)
        if not protocol:
            msg = af.PROTOCOL_EMPTY
            assert False

        cache_rule = handle_list(cache_rule)

        if CDNConf.HTTPS_TYPE in protocol and not cert_name:
            msg = af.CERT_NAME_EMPTY
            assert False

        check_domain = Domain.objects.filter(
            domain=domain, protocol__in=protocol).first()

        if check_domain:
            msg = af.DOMAIN_EXIST
            assert False

        src_ips = []
        src_domain = ''
        if src_type == CDNConf.SRC_IP:
            src_ips = src_value.split('\n')
        elif src_type == CDNConf.SRC_DOMAIN:
            src_domain = src_value

        if not src_host:
            src_host = domain

        src_back_ips = []
        src_back_domain = ''
        if src_back_type == CDNConf.SRC_BACK_IP:
            src_back_ips = src_back_value.split('\n')
        elif src_back_type == CDNConf.SRC_BACK_DOMAIN:
            src_back_domain = src_back_value

        body = {
            'base_template_id': CDNConf.BASE_CC_CMS_TEMPLATE_ID,
            'user_id': user.id,
            'domain': domain,
            'cdn_type': cdn_type,
            'contract_name': contract_name,
            'protocol': protocol,
            'cert_name': cert_name,
            'src_type': src_type,
            'src_ips': src_ips,
            'src_domain': src_domain,
            'src_host': src_host,
            'src_back_type': src_back_type,
            'src_back_ips': src_back_ips,
            'src_back_domain': src_back_domain,

            'ignore_cache_control': ignore_cache_control,
            'ignore_query_string': ignore_query_string,
            'cache_rule': cache_rule,
        }
        print(body)
        res = APIUrl.post_link('cdn_domain_create', body)
        print(res)
        return_code = res.get('return_code', 0)

        if return_code != 0:
            assert False

        for p in protocol:
            domain_obj = Domain(domain=domain, protocol=p, user=user)
            domain_obj.save()

        log_msg = om.CREATE_CDN_DOMAIN % (
            opt_user.username, user.username, domain)
        OperateLog.write_operate_log(request, om.ACCOUNTS, log_msg)

        status = True

    except AssertionError:
        pass

    return msg, status


def get_domain_log(request, user):
    """获取域名日志"""
    start_time = request.POST.get('start_time', 0)
    end_time = request.POST.get('end_time', 0)
    domain = request.POST.get('domain', '')

    msg = ''
    result_list = []
    pagination = {}

    try:
        msg, start_time, end_time = handle_req_time(start_time, end_time)
        if msg:
            assert False

        body = {
            'user_id': user.id,
            'start_time': start_time,
            'end_time': end_time,
            'domain': domain,

        }
        api_res = APIUrl.post_link('cdn_domain_log', body)
        return_code = api_res.get('return_code', 0)

        if return_code != 0:
            msg = af.PARAME_ERROR
            assert False

        result_list = api_res.get('result', [])

        all_log_list = []
        for channel in result_list:

            url_info = urlparse(channel)

            protocol = url_info.scheme

            log_list = result_list[channel]
            for log in log_list:
                # print(log['time'])
                """2019 10 14 20"""
                time_str = '%s-%s-%s %s:%s' % (
                    log['time'][:4], log['time'][4:6], log['time'][6:8],
                    log['time'][8:10], '00')

                log['time'] = time_str
                log['protocol'] = protocol

                all_log_list.append(log)

        result_list = sorted(
            all_log_list, key=lambda x: (x['time'], x['protocol']))

        msg, result_list, pagination = data_pagination(
            request, result_list)
    except AssertionError:
        pass

    return msg, result_list, pagination






