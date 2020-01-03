import time
import json
from copy import deepcopy
import asyncio
import os
import traceback
from urllib.parse import unquote

from django.http import StreamingHttpResponse, FileResponse, Http404
from django.utils.translation import ugettext as _


from common.feed import DEFAULT_RULE_CONF, WAF_ATTACK_TYPE
from common.country_conf import COUNTRY_NAME_CONF, COUNTRY_ABBREVIATION_CONF
from common.functions import (json_response, int_check, data_pagination,
                              file_iterator, timestamp_to_str, make_error_file)

from security.functions import make_base_excel, make_base_csv

from base.models import Domain, OperateLog

from common.feed import AccountsFeed as af, OperateMsg as om, APIUrl


def get_waf_defense_statistics(channel, flag_time):
    """获取waf数据"""

    body = {
        'channel': channel,
        'flag_time': flag_time
    }

    api_res = APIUrl.post_link('waf_defense_statistics', body)

    return api_res.get('data')


def user_get_waf_default_rule(request):
    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    provider = 'QINGSONG'

    domain_id = request.POST.get('domain_id', '')

    check_rule_id = request.POST.get('rule_id', '')
    check_rule_info = request.POST.get('rule_info', '')
    check_rule_status = request.POST.get('rule_status', '')

    is_en = False
    if request.LANGUAGE_CODE == 'en':
        is_en = True

    rule_list = []

    try:

        check_rule_info = check_rule_info.lower()

        if check_rule_id:
            check_rule_id = int_check(check_rule_id)
            if check_rule_id is None:
                msg = af.PARAME_ERROR
                assert False

        domain_obj = Domain.objects.filter(id=domain_id).first()
        if not domain_obj:
            msg = af.DOMAIN_NOT_EXIST
            assert False

        body = {
            'channel': '%s://%s' % (domain_obj.protocol, domain_obj.domain)
        }

        api_res = APIUrl.post_link('get_waf_default_rule', body)

        if api_res[provider]['return_code'] == 0:
            api_res = api_res[provider]

            rule_dict_list = api_res.get('data', [])

            for i in rule_dict_list:
                rule_id = int(i.get('rule_id', ''))

                if is_en:
                    temp_str = i['rule_info'].replace('\n', '').replace(' ', '')
                    i['rule_info'] = DEFAULT_RULE_CONF[
                        temp_str] if temp_str in DEFAULT_RULE_CONF else temp_str

                rule_info = i.get('rule_info', '')

                rule_info = rule_info.lower()

                rule_status = str(i.get('rule_status', '0'))

                if check_rule_id and check_rule_id != rule_id:
                    continue

                if check_rule_info and check_rule_info not in rule_info:
                    continue

                if check_rule_status and rule_status != check_rule_status:
                    continue

                rule_list.append(i)

            status = True

    except AssertionError:
        res['msg'] = _(msg)

    res['rule_list'] = rule_list
    res['status'] = status

    return json_response(res)


def user_get_waf_self_rule(request):

    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    provider = 'QINGSONG'

    domain_id = request.POST.get('domain_id', '')

    check_rule_name = request.POST.get('rule_name', '')
    check_rule_status = request.POST.get('rule_status', '')

    rule_list = []

    try:
        domain_obj = Domain.objects.filter(id=domain_id).first()
        if not domain_obj:
            msg = af.DOMAIN_NOT_EXIST
            assert False

        body = {
            'channel': '%s://%s' % (domain_obj.protocol, domain_obj.domain)
        }
        api_res = APIUrl.post_link('get_waf_self_rule', body)

        if api_res[provider]['return_code'] == 0:
            api_res = api_res[provider]

            rule_dict_list = api_res.get('data', [])

            for i in rule_dict_list.get('rule_list', []):
                rule_name = i.get('name', '')
                rule_status = str(i.get('enable', '0'))

                if check_rule_name and check_rule_name not in rule_name:
                    continue

                if check_rule_status and rule_status != check_rule_status:
                    continue

                rule_list.append(i)

            check_msg, rule_list, pagination = data_pagination(
                request, rule_list)

            if check_msg:
                res['msg'] = _(check_msg)
                return json_response(res)

            res['page_info'] = pagination

            status = True

    except AssertionError:
        res['msg'] = _(msg)

    res['rule_list'] = rule_list
    res['status'] = status

    return json_response(res)


def user_reset_default_rule(request):
    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    provider = 'QINGSONG'

    domain_id = request.POST.get('domain_id', '')
    enable = request.POST.get('enable', 0)

    try:
        domain_obj = Domain.objects.filter(id=domain_id).first()
        if not domain_obj:
            msg = af.DOMAIN_NOT_EXIST
            assert False

        body = {
            'channel': '%s://%s' % (domain_obj.protocol, domain_obj.domain),
        }

        enable = int_check(enable)
        if enable is None:
            msg = af.PARAME_ERROR
            assert False

        body['enable'] = enable
        api_res = APIUrl.post_link('reset_default_rule', body)
        if api_res[provider]['return_code'] == 0:
            status = True

            opt_msg = '全部开启' if enable else '全部关闭'
            log_msg = om.RESET_DEFAULT_RULE % (
                request.user.username, domain_obj.domain, opt_msg)
            OperateLog.write_operate_log(request, om.SECURITY, log_msg)

    except AssertionError:
        res['msg'] = _(msg)

    res['status'] = status

    return json_response(res)


def user_enable_default_rule(request):
    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }
    provider = 'QINGSONG'

    domain_id = request.POST.get('domain_id', '')
    rule_id = request.POST.get('rule_id', 0)
    enable = request.POST.get('enable', 0)

    try:
        domain_obj = Domain.objects.filter(id=domain_id).first()
        if not domain_obj:
            msg = af.DOMAIN_NOT_EXIST
            assert False

        body = {
            'channel': '%s://%s' % (domain_obj.protocol, domain_obj.domain),
        }

        enable = int_check(enable)
        if enable is None:
            msg = af.PARAME_ERROR
            assert False

        rule_id = int(rule_id)
        if rule_id is None:
            msg = af.PARAME_ERROR
            assert False

        body['enable'] = enable
        body['rule_id'] = rule_id
        api_res = APIUrl.post_link('enable_default_rule', body)

        if api_res[provider]['return_code'] == 0:
            status = True

            opt_msg = '开启' if enable else '关闭'
            log_msg = om.ENABLE_DEFAULT_RULE % (
                request.user.username, domain_obj.domain, rule_id, opt_msg)
            OperateLog.write_operate_log(request, om.SECURITY, log_msg)

    except AssertionError:
        res['msg'] = _(msg)

    res['status'] = status

    return json_response(res)


def user_enable_self_rule(request):
    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }
    provider = 'QINGSONG'

    domain_id = request.POST.get('domain_id', '')
    rule_id = request.POST.get('rule_id', 0)
    enable = request.POST.get('enable', 0)

    try:

        domain_obj = Domain.objects.filter(id=domain_id).first()
        if not domain_obj:
            msg = af.DOMAIN_NOT_EXIST
            assert False

        enable = int_check(enable)
        if enable is None:
            msg = af.PARAME_ERROR
            assert False

        rule_id = int(rule_id)
        if rule_id is None:
            msg = af.PARAME_ERROR
            assert False

        body = {
            'channel': '%s://%s' % (domain_obj.protocol, domain_obj.domain),
            'enable': enable,
            'rule_id': rule_id
        }

        api_res = APIUrl.post_link('enable_self_rule', body)

        print(api_res)

        if api_res[provider]['return_code'] == 0:
            status = True

            opt_msg = '开启' if enable else '关闭'
            log_msg = om.ENABLE_SELF_RULE % (
                request.user.username, rule_id, opt_msg)
            OperateLog.write_operate_log(request, om.SECURITY, log_msg)

    except AssertionError:
        res['msg'] = _(msg)

    res['status'] = status

    return json_response(res)


def user_get_log_list(request):
    """父账号自己查看日志"""

    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    is_en = False
    if request.LANGUAGE_CODE == 'en':
        is_en = True

    provider = 'QINGSONG'

    domain_id = request.POST.get('domain_id', '')
    atk_ip = request.POST.get('atk_ip', '')
    start_time = request.POST.get('start_time', 0)
    end_time = request.POST.get('end_time', 0)
    page = request.POST.get('page', 1)
    page_size = request.POST.get('size', 20)

    try:

        page = int_check(page)
        if page is None:
            msg = af.PARAME_ERROR
            assert False

        page = page - 1
        if page < 0:
            msg = af.PARAME_ERROR
            assert False

        domain_obj = Domain.objects.filter(id=domain_id).first()
        if not domain_obj:
            msg = af.DOMAIN_NOT_EXIST
            assert False

        body = {
            'channel': '%s://%s' % (domain_obj.protocol, domain_obj.domain),
            'start_time': start_time if start_time else None,
            'end_time': end_time if end_time else None,
            'atk_ip': atk_ip if atk_ip else None,
            'page': page,
            'page_size': page_size
        }
        api_res = APIUrl.post_link('waf_log_list', body)
        if api_res[provider]['return_code'] == 0:
            api_res = api_res[provider]
            status = True

            log_data = api_res.get('data', {})

            page_count = log_data.get('cur_page', 0)
            page_count += 1

            total = log_data.get('log_rows', 0)

            page_nums = log_data.get('page_cnt', 0)

            pagination = {
                'page_count': page_count,
                'page_nums': page_nums,
                'total': total
            }

            waf_log = log_data.get('waf_log', [])

            new_log_list = []
            for i in waf_log:
                atk_type = i.get('atk_type', '')
                if not is_en:
                    atk_type = WAF_ATTACK_TYPE[atk_type]
                i['atk_type'] = atk_type
                new_log_list.append(i)

            res['log_list'] = new_log_list
            res['page_info'] = pagination
            res['log_rows'] = log_data.get('log_rows', [])

    except AssertionError:
        res['msg'] = _(msg)

    res['status'] = status

    return json_response(res)


def user_get_log_detail(request):
    """父账号查看日志详情"""

    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    provider = 'QINGSONG'

    domain_id = request.POST.get('domain_id', '')
    log_id = request.POST.get('log_id', 0)
    log_time = request.POST.get('log_time', '')

    try:
        domain_obj = Domain.objects.filter(id=domain_id).first()
        if not domain_obj:
            msg = af.DOMAIN_NOT_EXIST
            assert False

        log_id = int_check(log_id)
        if log_id is None:
            msg = af.PARAME_ERROR
            assert False

        body = {
            'channel': '%s://%s' % (domain_obj.protocol, domain_obj.domain),
            'log_id': log_id,
            'log_time': log_time
        }

        api_res = APIUrl.post_link('waf_log_detail', body)

        if api_res[provider]['return_code'] == 0:
            api_res = api_res[provider]
            status = True

            detail_data = api_res.get('data', {})

            res['detail_data'] = detail_data

    except AssertionError:
        res['msg'] = _(msg)

    res['status'] = status

    return json_response(res)


def user_download_log(request, domain_id, atk_ip,
                        start_time, end_time, log_rows):
    """父账号下载日志
    {'action': 'waf_report', 'message': 'success',
    'data': {'cur_page': 70, 'log_rows': 1381, 'waf_log': [], 'page_cnt': 70},
    'return_code': 0}
    """
    msg = ''
    status = False

    page_size = 2000

    log_list = []

    is_en = False
    if request.LANGUAGE_CODE == 'en':
        is_en = True

    provider = 'QINGSONG'

    try:

        log_rows = int_check(log_rows)
        if log_rows is None:
            msg = af.PARAME_ERROR
            assert False

        page_count = log_rows // page_size

        domain_id = int(domain_id)
        domain_obj = Domain.objects.filter(id=domain_id).first()
        if not domain_obj:
            msg = af.DOMAIN_NOT_EXIST
            assert False

        channel = '%s://%s' % (domain_obj.protocol, domain_obj.domain)

        body = {
            'channel': channel,
        }

        if start_time and end_time:

            start_time = int_check(start_time)
            if start_time is None:
                msg = af.PARAME_ERROR
                assert False

            end_time = int_check(end_time)
            if end_time is None:
                msg = af.PARAME_ERROR
                assert False

            base_format = '%Y-%m-%d %H:%M'
            start_time = timestamp_to_str(start_time, _format=base_format)
            end_time = timestamp_to_str(end_time, _format=base_format)

            body['start_time'] = start_time
            body['end_time'] = end_time

        if atk_ip != '-':
            body['atk_ip'] = atk_ip

        body_list = []
        for count in range(0, page_count+1):
            body['page'] = count
            body['page_size'] = page_size
            body_list.append(deepcopy(body))
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        p0 = time.time()
        r = loop.run_until_complete(asyncio.wait([APIUrl.doPostAio('waf_log_list', b) for b in body_list]))
        p1 = time.time()
        print(f'user_download_log[len: {len(body_list)}.] takeTime: {p1-p0}')
        results = r[0]

        n = 0
        for i in results:
            try:
                result = json.loads(i.result())
                data = result.get(provider).get('data')
                if result.get(provider).get('return_code') == 0:
                    log_list.extend(data['waf_log'])
                    print(f'user_download_log[No.{n}] cur_page: {data["cur_page"]}|| log_rows: {data["log_rows"]}')
            except json.decoder.JSONDecodeError:
                print(f'user_download_log[jsonError.] error: {i.result()}|| info: {r[1]}|| traceback: {traceback.format_exc()}')

                # api_res = APIUrl.post_link('waf_log_list', body)
                # if api_res[provider]['return_code'] == 0:
                #     api_res = api_res[provider]
                #     waf_log = api_res.get('data', {}).get('waf_log', [])
                #     log_list.extend(waf_log)

            n += 1
        loop.close()

            # api_res = APIUrl.post_link('waf_log_list', body)

            # if api_res[provider]['return_code'] == 0:
            #     api_res = api_res[provider]

            #     waf_log = api_res.get('data', {}).get('waf_log', [])

            #     log_list.extend(waf_log)

        # ---origins as below
        # for count in range(0, page_count+1):
        #     body['page'] = count
        #     body['page_size'] = page_size

        #     api_res = APIUrl.post_link('waf_log_list', body)

        #     if api_res[provider]['return_code'] == 0:
        #         api_res = api_res[provider]

        #         waf_log = api_res.get('data', {}).get('waf_log', [])

        #         log_list.extend(waf_log)

        # excel_name = '%s-log.xlsx' % domain_obj.domain
        # sheet_name = 'log_data'
        # row, excel_path, worksheet, workbook = make_base_excel(excel_name, sheet_name, channel, start_time, end_time)

        csv_rows = [['waf_channel:', channel], ['start_time:', start_time], ['end_time:', end_time], [], []]
        csv_header = ['log_time', 'atk_ip', 'tar_url', 'atk_url', 'rule_id']
        csv_rows.append(csv_header)

        csv_name = '%s-log.csv' % domain_obj.domain
        for v in log_list:
            log_time = v.get('log_time', '')
            atk_ip = v.get('atk_ip', '')
            target_url = v.get('target_url', '')
            # target_url = unquote(target_url)

            atk_type = v.get('atk_type', '')
            # if not is_en:
            #     # atk_type = WAF_ATTACK_TYPE[atk_type].encode('utf-8').decode('gb18030')
            #     atk_type = WAF_ATTACK_TYPE[atk_type]
            #     # try:
            #     #     atk_type = WAF_ATTACK_TYPE[atk_type].encode('utf-8').decode('GB2312')
            #     # except UnicodeDecodeError:
            #     #     print(f'\n---atk_type(Error.)---\n{atk_type}')
            #     #     atk_type = WAF_ATTACK_TYPE[atk_type]

            rule_id = v.get('ruleid', '')

            csv_rows.append([log_time, atk_ip, target_url, atk_type, rule_id])
        csv_path = make_base_csv(csv_name, csv_rows)

        # print(f'\n---"Done."---\n{"Done."}')
        # assert False


        # row += 3

        # worksheet.write(row, 0, label='log_time')
        # worksheet.write(row, 1, label='atk_ip')
        # worksheet.write(row, 2, label='tar_url')
        # worksheet.write(row, 3, label='atk_type')
        # worksheet.write(row, 4, label='rule_id')

        # base_rote = 40

        # for v in log_list:
        #     row += 1
        #     log_time = v.get('log_time', '')
        #     atk_ip = v.get('atk_ip', '')
        #     target_url = v.get('target_url', '')
        #     target_url = unquote(target_url)

        #     atk_type = v.get('atk_type', '')
        #     if not is_en:
        #         atk_type = WAF_ATTACK_TYPE[atk_type]

        #     rule_id = v.get('ruleid', '')

        #     if len(target_url) > base_rote:
        #         first_col = worksheet.col(2)
        #         first_col.width = 100 * len(target_url) if 100 * len(target_url) < 65536 else 60000
        #         base_rote = len(target_url)

        #     worksheet.write(row, 0, label=log_time)
        #     worksheet.write(row, 1, label=atk_ip)
        #     worksheet.write(row, 2, label=target_url)
        #     worksheet.write(row, 3, label=atk_type)
        #     worksheet.write(row, 4, label=rule_id)

        # workbook.save(excel_path)

    except AssertionError:
        csv_name = 'error_documents'
        csv_path = make_error_file(csv_name, _(msg))

    # response = StreamingHttpResponse(file_iterator(csv_path))
    try:
        response = FileResponse(open(csv_path, 'rb'))

        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = f'attachment;filename="{csv_name}"'

        os.remove(csv_path)
        print(f'user_download_log[FileDeleteDone.] csv_path: {csv_path}')

        return response
    except Exception:
        print(f'user_download_log[Error.] error: {traceback.format_exc()}')
        raise Http404


def user_get_waf_statistics(request):
    """父账号查看统计数据"""
    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    provider = 'QINGSONG'

    is_en = False
    if request.LANGUAGE_CODE == 'en':
        is_en = True

    domain_id = request.POST.get('domain_id', '')
    start_time = request.POST.get('start_time', '')
    end_time = request.POST.get('end_time', '')

    try:
        domain_obj = Domain.objects.filter(id=domain_id).first()
        if not domain_obj:
            msg = af.DOMAIN_NOT_EXIST
            assert False

        body = {
            'channel': '%s://%s' % (domain_obj.protocol, domain_obj.domain),
            'start_day': start_time,
            'end_day': end_time,
        }
        api_res = APIUrl.post_link('waf_defense_statistics', body)

        if api_res[provider]['return_code'] == 0:
            api_res = api_res[provider]
            status = True

            detail_data = api_res.get('data', {})

            ip_list = detail_data.get('ip_list', [])
            new_ip = []
            for i in ip_list:
                ip_address = i.get('ip_address', '')

                if is_en:
                    if ip_address in COUNTRY_NAME_CONF:

                        i['ip_address'] = COUNTRY_NAME_CONF[ip_address]
                    else:
                        i['ip_address'] = 'Unknown'

                i['short_name'] = COUNTRY_ABBREVIATION_CONF[ip_address] \
                    if ip_address in COUNTRY_ABBREVIATION_CONF else ''
                new_ip.append(i)
            detail_data['ip_list'] = new_ip

            rule_list = detail_data.get('rule_list', [])

            new_rule_list = []
            for i in rule_list:
                name = i.get('name', '')
                if name == '剩余':
                    i['name'] = 'Other'

                new_rule_list.append(i)
            detail_data['rule_list'] = new_rule_list

            if request.LANGUAGE_CODE == 'zh-hans':

                new_rule_list = []
                for i in rule_list:
                    name = i.get('name', '')
                    if name in WAF_ATTACK_TYPE:
                        i['name'] = WAF_ATTACK_TYPE[name]

                    new_rule_list.append(i)

                detail_data['rule_list'] = new_rule_list

            new_time_cnt = []
            time_cnt_data = detail_data.get('time_cnt', [])
            time_str_list = list(time_cnt_data.keys())

            time_str_list.sort()
            total_attack_cnt = 0
            for time_key in time_str_list:
                data_list = time_cnt_data[time_key]

                day_str = '%s-%s-%s' % (
                    time_key[:4], time_key[4:6], time_key[6:8])

                for v in data_list:
                    cnt = v.get('cnt', 0)
                    total_attack_cnt += cnt

                    name = int(v.get('name'))

                    hour_str = '0%s:00' % name \
                        if int(name) < 10 else '%s:00' % name

                    time_str = '%s %s' % (day_str, hour_str)

                    new_time_cnt.append({'cnt': cnt, 'name': time_str})

            detail_data['time_cnt'] = new_time_cnt
            detail_data['total_attack_cnt'] = total_attack_cnt

            if 'region_info' in detail_data:
                detail_data.pop('region_info')
            if 'waf_def' in detail_data:
                detail_data.pop('waf_def')
            if 'default_def' in detail_data:
                detail_data.pop('default_def')
            if 'custom_def' in detail_data:
                detail_data.pop('custom_def')
            if 'site_list' in detail_data:
                detail_data.pop('site_list')

            res['statistics_data'] = detail_data

    except AssertionError:
        res['msg'] = _(msg)

    res['status'] = status

    return json_response(res)


def user_download_time_cnt(request, domain_id, start_time, end_time):
    """父账号下载拦截攻击次数excel"""
    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    provider = 'QINGSONG'

    domain_obj = Domain.objects.filter(id=domain_id).first()

    try:
        if not domain_obj:
            msg = af.DOMAIN_NOT_EXIST
            assert False

        excel_name = '%s-time_cut.xls' % domain_obj.domain

        start_time = int_check(start_time)
        if start_time is None:
            msg = af.PARAME_ERROR
            assert False

        end_time = int_check(end_time)
        if end_time is None:
            msg = af.PARAME_ERROR
            assert False

        start_time = timestamp_to_str(start_time, _format='%Y-%m-%d')
        end_time = timestamp_to_str(end_time, _format='%Y-%m-%d')

        channel = '%s://%s' % (domain_obj.protocol, domain_obj.domain)

        body = {
            'channel': channel,
            'start_day': start_time,
            'end_day': end_time,
        }

        api_res = APIUrl.post_link('waf_defense_statistics', body)

        if api_res[provider]['return_code'] == 0:
            api_res = api_res[provider]
            sheet_name = 'time-cut'

            row, excel_path, worksheet, workbook = make_base_excel(
                excel_name, sheet_name, channel, start_time, end_time)

            detail_data = api_res.get('data', {})

            time_cnt_data = detail_data.get('time_cnt', [])

            row += 3

            worksheet.write(row, 0, label='time')
            worksheet.write(row, 1, label='count')

            time_str_list = list(time_cnt_data.keys())

            time_str_list.sort()

            for time_key in time_str_list:
                data_list = time_cnt_data[time_key]

                day_str = '%s-%s-%s' % (
                    time_key[:4], time_key[4:6], time_key[6:8])

                for v in data_list:
                    row += 1
                    cnt = v.get('cnt', 0)
                    name = int(v.get('name'))

                    name = '0%s' % name if name < 10 else str(name)
                    start = '%s:00' % name
                    end = '%s:59' % name

                    time_str = '%s %s - %s %s' % (day_str, start, day_str, end)

                    worksheet.write(row, 0, label=time_str)
                    worksheet.write(row, 1, label=cnt)

            workbook.save(excel_path)

    except AssertionError:
        excel_name = 'error_documents'
        excel_path = make_error_file(excel_name, _(msg))

    response = StreamingHttpResponse(file_iterator(excel_path))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(
        excel_name)

    return response


def user_download_ip_list(request, domain_id, start_time, end_time):
    """父账号下载拦截攻击来源"""
    msg = ''
    status = False

    is_en = False
    if request.LANGUAGE_CODE == 'en':
        is_en = True

    res = {
        'status': status,
        'msg': msg
    }

    provider = 'QINGSONG'

    try:
        start_time = int_check(start_time)
        if start_time is None:
            msg = af.PARAME_ERROR
            assert False

        end_time = int_check(end_time)
        if end_time is None:
            msg = af.PARAME_ERROR
            assert False

        start_time = timestamp_to_str(start_time, _format='%Y-%m-%d')
        end_time = timestamp_to_str(end_time, _format='%Y-%m-%d')

        domain_obj = Domain.objects.filter(id=domain_id).first()
        if not domain_obj:
            msg = af.DOMAIN_NOT_EXIST
            assert False

        channel = '%s://%s' % (domain_obj.protocol, domain_obj.domain)

        body = {
            'channel': channel,
            'start_day': start_time,
            'end_day': end_time,
        }

        api_res = APIUrl.post_link('waf_defense_statistics', body)

        excel_name = '%s-ip_list.xls' % domain_obj.domain

        if api_res[provider]['return_code'] == 0:
            api_res = api_res[provider]

            detail_data = api_res.get('data', {})

            ip_list = detail_data.get('ip_list', [])

            sheet_name = 'ip-list'

            row, excel_path, worksheet, workbook = make_base_excel(
                excel_name, sheet_name, channel, start_time, end_time)

            row += 3

            worksheet.write(row, 0, label='ip_address')
            worksheet.write(row, 1, label='count')

            for v in ip_list:
                row += 1
                ip = v.get('ip', '')
                ip_address = v.get('ip_address', '')

                if is_en:
                    if ip_address in COUNTRY_NAME_CONF:
                        ip_address = COUNTRY_NAME_CONF[ip_address]
                    else:
                        ip_address = 'Unknown'

                cnt = v.get('cnt', '')
                worksheet.write(row, 0, label=ip)
                worksheet.write(row, 1, label=ip_address)
                worksheet.write(row, 2, label=cnt)

            workbook.save(excel_path)

    except AssertionError:
        excel_name = 'error_documents'
        excel_path = make_error_file(excel_name, _(msg))

    response = StreamingHttpResponse(file_iterator(excel_path))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(
        excel_name)

    return response


def user_download_rule_list(request, domain_id, start_time, end_time):
    """父账号下载攻击方式"""

    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    provider = 'QINGSONG'

    try:
        start_time = int_check(start_time)
        if start_time is None:
            msg = af.PARAME_ERROR
            assert False

        end_time = int_check(end_time)
        if end_time is None:
            msg = af.PARAME_ERROR
            assert False

        start_time = timestamp_to_str(start_time, _format='%Y-%m-%d')
        end_time = timestamp_to_str(end_time, _format='%Y-%m-%d')

        domain_obj = Domain.objects.filter(id=domain_id).first()
        if not domain_obj:
            msg = af.DOMAIN_NOT_EXIST
            assert False

        channel = '%s://%s' % (domain_obj.protocol, domain_obj.domain)

        body = {
            'channel': channel,
            'start_day': start_time,
            'end_day': end_time,
        }

        api_res = APIUrl.post_link('waf_defense_statistics', body)

        excel_name = '%s-rule_list.xls' % domain_obj.domain

        if api_res[provider]['return_code'] == 0:
            api_res = api_res[provider]

            detail_data = api_res.get('data', {})

            sheet_name = 'rule-list'

            url_list = detail_data.get('url_list', [])

            row, excel_path, worksheet, workbook = make_base_excel(
                excel_name, sheet_name, channel, start_time, end_time)

            row += 3

            worksheet.write(row, 0, label='type')
            worksheet.write(row, 1, label='count')
            worksheet.write(row, 2, label='proportion(%)')

            rule_list = detail_data.get('rule_list', [])

            for v in rule_list:
                row += 1
                name = v.get('name', '')
                cnt = v.get('cnt', '')
                pro = v.get('pro', '')
                worksheet.write(row, 0, label=name)
                worksheet.write(row, 1, label=cnt)
                worksheet.write(row, 2, label=pro)

            row += 5
            worksheet.write(row, 0, label='url')
            worksheet.write(row, 1, label='count')

            base_rote = 40

            for v in url_list:
                row += 1
                site_url = v.get('site_url', '')
                site_url = unquote(site_url)

                if len(site_url) > base_rote:
                    first_col = worksheet.col(0)
                    first_col.width = 256 * len(site_url)
                    base_rote = len(site_url)

                cnt = v.get('cnt', '')
                worksheet.write(row, 0, label=site_url)
                worksheet.write(row, 1, label=cnt)

            workbook.save(excel_path)

    except AssertionError:
        excel_name = 'error_documents'
        excel_path = make_error_file(excel_name, _(msg))

    response = StreamingHttpResponse(file_iterator(excel_path))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(
        excel_name)

    return response