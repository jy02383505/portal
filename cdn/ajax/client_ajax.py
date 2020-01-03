
import json
from urllib.parse import urlparse

from django.http import StreamingHttpResponse
from django.utils.translation import ugettext as _
from django.views.decorators.gzip import gzip_page
from django.contrib.auth.decorators import login_required

from common.decorators import rights_required
from common.feed import (AccountsFeed as af, OperateMsg as om, APIUrl, CDNConf,
                         CertConf)
from common.functions import (json_response, int_check, data_pagination,
                              make_error_file, file_iterator, timestamp_to_str,
                              datetime_correction, get_this_month_time,
                              datetime_to_timestamp, handle_list,
                              handle_req_time)

from base.models import Domain, OperateLog
from cdn.ajax.base_ajax import (get_domain_flux, get_domain_request,
                                get_domain_status_code, get_domain_list,
                                user_domain_refresh, user_domain_refresh_status,
                                user_domain_preload, user_domain_preload_status,
                                user_domain_create, get_domain_log)
from cdn.funcions import make_base_excel


@login_required
@rights_required('client_cdn_domain_list')
def client_get_domain_list(request):
    """客户端获取域名列表"""
    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }
    user = request.user

    domain = request.POST.get('domain', '')
    cdn_type = request.POST.get('cdn_type', '')
    domain_status = request.POST.get('domain_status', '[]')

    domain_query = Domain.get_domain_query_by_user(user)


    try:
        domain_status = handle_list(domain_status, dec_int=True)

        if domain:
            domain_query = domain_query.filter(domain=domain)

        domain_query = domain_query.order_by('-protocol')

        check_msg, domain_dict_list, pagination = get_domain_list(
            request, domain_query, cdn_type, domain_status)

        if check_msg:
            res['msg'] = check_msg
            return json_response(res)

        res['domain_list'] = domain_dict_list
        res['page_info'] = pagination

        status = True

    except AssertionError:
        res['msg'] = msg
        return json_response(res)

    res['status'] = status

    return json_response(res)


@login_required
@rights_required('client_cdn_create_domain')
def client_cdn_domain_disable(request):
    """客户端域名报停"""
    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    user = request.user

    domain_list = request.POST.get('domain', '[]')

    # domain = '[itestxz0018.chinacache.com]'

    try:
        domain_list = json.loads(domain_list)

        body = {
            'domain': domain_list,
            'user_id': user.id,

        }
        api_res = APIUrl.post_link('cdn_domain_disable', body)
        assert api_res
        return_code = api_res.get('return_code', 0)

        if return_code != 0:
            assert False

        status = True

        domain_str = ','.join(domain_list)
        log_msg = om.DISABLE_CDN_DOMAIN % (
            user.username, user.username, domain_str)
        OperateLog.write_operate_log(request, om.ACCOUNTS, log_msg)

    except Exception as e:
        print(e)
        res['msg'] = _(msg)

    res['status'] = status

    return json_response(res)


@login_required
@rights_required('client_cdn_create_domain')
def client_cdn_domain_active(request):
    """客户端域名激活"""
    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    user = request.user

    domain_list = request.POST.get('domain', '[]')
    # domain = '[itestxz0018.chinacache.com]'

    try:
        domain_list = json.loads(domain_list)

        body = {
            'domain': domain_list,
            'user_id': user.id,

        }
        api_res = APIUrl.post_link('cdn_domain_active', body)
        assert api_res
        return_code = api_res.get('return_code', 0)

        if return_code != 0:
            assert False

        status = True

        domain_str = ','.join(domain_list)
        log_msg = om.ACTIVE_CDN_DOMAIN % (
            user.username, user.username, domain_str)
        OperateLog.write_operate_log(request, om.ACCOUNTS, log_msg)

    except Exception as e:
        print(e)
        res['msg'] = _(msg)

    res['status'] = status

    return json_response(res)


@login_required
@rights_required('client_cdn_create_domain')
def client_cdn_create_domain(request):
    """
    客户端创建cdn域名
    """
    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    user = request.user

    try:
        msg, status = user_domain_create(request, user, user)

        if not status:
            assert False

    except AssertionError:
        res['msg'] = _(msg)
    except Exception as e:
        print(e)

    res['status'] = status

    return json_response(res)


@login_required
@rights_required('client_cdn_create_domain')
def client_cdn_edit_domain(request):
    """
    客户端修改cdn域名
    """
    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    user = request.user

    domain = request.POST.get('domain', '')

    cert_name = request.POST.get('cert_name', '')
    src_type = request.POST.get('src_type', '')
    src_value = request.POST.get('src_value', '')
    src_host = request.POST.get('src_host', '')

    src_back_type = request.POST.get('src_back_type', '')
    src_back_value = request.POST.get('src_back_value', '')

    ignore_cache_control = request.POST.get('ignore_cache_control', '0')
    ignore_query_string = request.POST.get('ignore_query_string', '0')

    cache_rule = request.POST.get('cache_rule', '[]')

    try:
        cache_rule = json.loads(cache_rule)

        if src_back_value and not src_back_type:
            msg = af.SRC_BACK_TYPE_EMPTY
            assert False

        check_domain = Domain.objects.filter(domain=domain).first()
        if not check_domain:
            assert False
            msg = af.DOMAIN_NOT_EXIST

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
            'user_id': user.id,
            'domain': domain,
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
        api_res = APIUrl.post_link('cdn_domain_edit', body)
        print(api_res)
        return_code = api_res.get('return_code', 0)

        if return_code != 0:
            assert False

        status = True

        log_msg = om.EDIT_CDN_DOMAIN % (user.username, user.username, domain)
        OperateLog.write_operate_log(request, om.ACCOUNTS, log_msg)

    except Exception as e:
        print(e)
        res['msg'] = _(msg)

    res['status'] = status

    return json_response(res)


@login_required
@rights_required('client_cdn_domain_statistical')
@gzip_page
def client_cdn_flux_data(request):
    """客户端查看计费状态码统计数据"""
    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    user = request.user

    start_time = request.POST.get('start_time', 0)
    end_time = request.POST.get('end_time', 0)
    domain_ids = request.POST.get('domain_list', '[]')

    all_flux_list = []    # 计费图表数据
    sum_cdn_flux = 0    # 总计费数据(MB)
    sum_src_flux = 0    # 总回源数据(MB)
    max_cdn = 0    # 峰值计费值(M/bps)

    table_data = []    # 每日表格数据


    try:
        msg, start_time, end_time = handle_req_time(start_time, end_time)
        if msg:
            assert False

        domain_ids = handle_list(domain_ids, dec_int=True)
        if domain_ids:
            domain_query = Domain.objects.filter(id__in=domain_ids)
        else:
            domain_query = Domain.objects.filter(user=user)

        domain_list = [i.domain for i in domain_query]
        if domain_list:

            opts = []

            (all_flux_list, sum_cdn_flux, sum_src_flux,
             max_cdn, max_src, table_data, __) = get_domain_flux(
                user.id, domain_list, start_time, end_time, opts)

        status = True
    except Exception as e:
        print(e)
        res['msg'] = _(msg)


    res['status'] = status
    res['domain_flux'] = all_flux_list
    res['sum_cdn_flux'] = sum_cdn_flux
    res['sum_src_flux'] = sum_src_flux
    res['max_cdn'] = max_cdn
    res['table_data'] = table_data

    return json_response(res)


@login_required
@rights_required('client_cdn_domain_statistical')
@gzip_page
def client_cdn_request_data(request):
    """管理员查看请求量统计数据"""

    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    user = request.user

    start_time = request.POST.get('start_time', 0)
    end_time = request.POST.get('end_time', 0)
    domain_ids = request.POST.get('domain_list', '[]')

    request_ratio = 0    # 请求命中率(%)
    opts = []

    try:
        msg, start_time, end_time = handle_req_time(start_time, end_time)
        if msg:
            assert False

        domain_ids = handle_list(domain_ids, dec_int=True)
        if domain_ids:
            domain_query = Domain.objects.filter(id__in=domain_ids)
        else:
            domain_query = Domain.objects.filter(user=user)

        domain_list = [i.domain for i in domain_query]

        if domain_ids:
            request_ratio = get_domain_request(
                user.id, domain_list, start_time, end_time, opts)

        status = True
    except Exception as e:
        print(e)
        res['msg'] = _(msg)

    res['status'] = status
    res['request_ratio'] = request_ratio

    return json_response(res)


@login_required
@rights_required('client_cdn_domain_statistical')
def client_download_cdn_flux(request, start_time, end_time, domain_ids):
    """下载计费数据"""

    msg = ''
    status = False

    try:
        user = request.user

        msg, start_time, end_time = handle_req_time(start_time, end_time)
        if msg:
            assert False

        if domain_ids == '-':
            domain_query = Domain.objects.filter(user=user)
        else:
            domain_ids = domain_ids.split(',')
            domain_query = Domain.objects.filter(id__in=domain_ids)

        domain_list = [i.domain for i in domain_query]

        opts = []

        (all_flux_list, sum_cdn_flux, sum_src_flux,
         max_cdn, max_src, table_data, opt_result) = get_domain_flux(
            user.id, domain_list, start_time, end_time, opts)

        excel_name = '%s-flux_data.xls' % user.username
        sheet_name = 'Detailed Traffic Bandwidth'

        start_time = timestamp_to_str(start_time)
        end_time = timestamp_to_str(end_time)

        row, excel_path, worksheet, workbook = make_base_excel(
            excel_name, sheet_name, domain_list, start_time, end_time)

        row += 1
        worksheet.write(row, 0, label='Peak bandwidth (Mbps)')
        worksheet.write(row, 1, label=max_cdn)

        row += 1
        worksheet.write(row, 0, label='Source peak bandwidth (Mbps)')
        worksheet.write(row, 1, label=max_src)

        row += 1
        worksheet.write(row, 0, label='Total flow (MB)')
        worksheet.write(row, 1, label=sum_cdn_flux)

        row += 1
        worksheet.write(row, 0, label='Total source flow (MB)')
        worksheet.write(row, 1, label=sum_src_flux)

        row += 2
        worksheet.write(row, 0, label='Time')
        worksheet.write(row, 1, label='bandwidth (Mbps)')
        worksheet.write(row, 2, label='flow (MB)')

        row += 1
        for i in all_flux_list:
            time_key = i.get('time_key', '')
            cdn_data = i.get('cdn_data', 0)

            cdn_bandwidth = cdn_data / 300 * 8

            worksheet.write(row, 0, label=time_key)
            worksheet.write(row, 1, label=cdn_bandwidth)
            worksheet.write(row, 2, label=cdn_data)

            row += 1

        workbook.save(excel_path)

    except AssertionError:
        excel_name = 'error_documents'
        excel_path = make_error_file(excel_name, _(msg))

    response = StreamingHttpResponse(file_iterator(excel_path))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(
        excel_name)

    return response


@login_required
@rights_required('client_cdn_domain_statistical')
@gzip_page
def client_cdn_status_code_data(request):
    """客户端查看状态码统计数据"""
    import time
    start = time.time()
    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    user = request.user

    start_time = request.POST.get('start_time', 0)
    end_time = request.POST.get('end_time', 0)
    domain_ids = request.POST.get('domain_list', '[]')

    base_code = CDNConf.STATUS_CODE

    all_status_code = []    # 全部状态码数据
    status_code_table = []    # 状态码表格数据

    all_trend_result = []

    trend_table_data = []

    try:
        msg, start_time, end_time = handle_req_time(start_time, end_time)
        if msg:
            assert False

        domain_ids = handle_list(domain_ids, dec_int=True)

        if domain_ids:
            domain_query = Domain.objects.filter(id__in=domain_ids)
        else:
            domain_query = Domain.objects.filter(user=user)

        domain_list = [i.domain for i in domain_query]

        if domain_list:

            (all_status_code, __, all_trend_result,
             all_trend_data, __) = get_domain_status_code(
                user.id, domain_list, start_time, end_time, [])

            sum_req = 0
            for code in all_status_code:
                sum_req += all_status_code[code]

            for code in base_code:
                num = all_status_code[code]
                ratio = (num / sum_req) * 100 if sum_req else 0

                code_dict = {
                    'code': code,
                    'num': num,
                    'ratio': '%.4f' % ratio
                }
                status_code_table.append(code_dict)

            trend_key = list(all_trend_data.keys())
            trend_key.sort()

            sum_cnt = 0
            for i in all_trend_data:
                sum_cnt += all_trend_data[i]

            for key in trend_key:
                code_cnt = all_trend_data[key]

                ratio = code_cnt / sum_cnt * 100 if sum_cnt else 0

                temp_dict = {
                    'code': key,
                    'count': code_cnt,
                    'ratio': '%.4f' % ratio
                }
                trend_table_data.append(temp_dict)

        status = True

    except Exception as e:
        print(e)
        res['msg'] = _(msg)

    print(444444444, time.time()-start)
    res['all_status_code'] = all_status_code
    res['status_code_table'] = status_code_table

    res['all_trend_result'] = all_trend_result
    res['all_trend_data'] = trend_table_data
    res['status'] = status

    return json_response(res)


@login_required
@rights_required('client_cdn_domain_statistical')
def client_download_status_code(request, start_time, end_time, domain_ids):
    """下载计费数据"""

    msg = ''
    status = False

    base_code = CDNConf.STATUS_CODE

    try:
        user = request.user

        msg, start_time, end_time = handle_req_time(start_time, end_time)
        if msg:
            assert False

        if domain_ids == '-':
            domain_query = Domain.objects.filter(user=user)
        else:
            domain_ids = domain_ids.split(',')
            domain_query = Domain.objects.filter(id__in=domain_ids)

        domain_list = [i.domain for i in domain_query]

        opts = []

        all_status_code, __, __, __, __ = get_domain_status_code(
            user.id, domain_list, start_time, end_time, opts)

        excel_name = '%s-status_code.xls' % user.username
        sheet_name = 'status_code'

        start_time = timestamp_to_str(start_time)
        end_time = timestamp_to_str(end_time)

        row, excel_path, worksheet, workbook = make_base_excel(
            excel_name, sheet_name, domain_list, start_time, end_time)

        base_row = row + 2
        worksheet.write(base_row, 0, label='status_code')
        worksheet.write(base_row, 1, label='total')
        worksheet.write(base_row, 2, label='Percentage')

        row += 3
        """
        {'200': 2528161, '206': 34, '302': 0, '304': 41,
        '403': 0, '404': 0, '5xx': 0, 'other': 1}
        {'CC': {'200': 2528161, '206': 34, '302': 0, '304': 41,
        '403': 0, '404': 0, '5xx': 0, 'other': 1}}

        """

        sum_req = 0
        for i in all_status_code:
            sum_req += all_status_code[i]

        for code in base_code:
            num = all_status_code[code]
            ratio = '%.4f' %(num / sum_req * 100)

            worksheet.write(row, 0, label=code)
            worksheet.write(row, 1, label=num)
            worksheet.write(row, 2, label='{}%'.format(ratio))

            row += 1

        workbook.save(excel_path)

    except AssertionError:
        excel_name = 'error_documents'
        excel_path = make_error_file(excel_name, _(msg))

    response = StreamingHttpResponse(file_iterator(excel_path))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(
        excel_name)

    return response


@login_required
@rights_required('client_cdn_domain_statistical')
def client_download_status_code_trend(
        request, start_time, end_time, domain_ids):
    """下载计费数据"""

    msg = ''
    status = False

    base_code = CDNConf.STATUS_CODE_TREND

    try:
        user = request.user

        msg, start_time, end_time = handle_req_time(start_time, end_time)
        if msg:
            assert False

        if domain_ids == '-':
            domain_query = Domain.objects.filter(user=user)
        else:
            domain_ids = domain_ids.split(',')
            domain_query = Domain.objects.filter(id__in=domain_ids)

        domain_list = [i.domain for i in domain_query]

        opts = []


        __, __, __, all_trend_data, __ = get_domain_status_code(
            user.id, domain_list, start_time, end_time, opts)

        excel_name = '%s-status_code_trend.xls' % user.username
        sheet_name = 'status_code_trend'

        start_time = timestamp_to_str(start_time)
        end_time = timestamp_to_str(end_time)

        row, excel_path, worksheet, workbook = make_base_excel(
            excel_name, sheet_name, domain_list, start_time, end_time)

        base_row = row + 2
        worksheet.write(base_row, 0, label='status_code')
        worksheet.write(base_row, 1, label='total')
        worksheet.write(base_row, 2, label='Percentage')

        row += 3
        """
        {'2xx': 2528195, '3xx': 41, '4xx': 1, '5xx': 0}
        {'CC': {'2xx': 2528195, '3xx': 41, '4xx': 1, '5xx': 0}}
        """

        sum_req = 0
        for i in all_trend_data:
            sum_req += all_trend_data[i]

        for code in base_code:
            num = all_trend_data[code]
            ratio = '%.4f' %(num / sum_req * 100)

            worksheet.write(row, 0, label=code)
            worksheet.write(row, 1, label=num)
            worksheet.write(row, 2, label='{}%'.format(ratio))

            row += 1

        workbook.save(excel_path)

    except AssertionError:
        excel_name = 'error_documents'
        excel_path = make_error_file(excel_name, _(msg))

    response = StreamingHttpResponse(file_iterator(excel_path))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(
        excel_name)

    return response


@login_required
@rights_required('client_cdn_domain_refresh')
def client_cdn_domain_refresh(request):
    """客户端url刷新"""
    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    user = request.user

    try:
        msg = user_domain_refresh(request, user)
        if msg:
            assert False

        status = True
    except AssertionError:
        res['msg'] = _(msg)

    res['status'] = status

    return json_response(res)


@login_required
@rights_required('client_cdn_domain_refresh')
def client_cdn_domain_refresh_status(request):
    """客户端url刷新查询"""
    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    user = request.user

    try:
        msg, result_list, pagination = user_domain_refresh_status(request, user)

        if msg:
            assert False

        res['refresh_log_list'] = result_list
        res['page_info'] = pagination

        status = True
    except Exception as e:
        print(e)
        res['msg'] = _(msg)

    res['status'] = status

    return json_response(res)


@login_required
@rights_required('client_cdn_domain_preload')
def client_cdn_domain_preload(request):
    """客户端url预热"""
    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }
    print(11111111, request.POST)
    user = request.user

    try:
        msg = user_domain_preload(request, user)

        if msg:
            assert False

        status = True
    except Exception as e:
        print(e)
        res['msg'] = _(msg)

    res['status'] = status

    return json_response(res)


@login_required
@rights_required('client_cdn_domain_preload')
def client_cdn_domain_preload_status(request):
    """客户端url预热查询"""
    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }
    user = request.user
    try:
        msg, result_list, pagination = user_domain_preload_status(request, user)

        if msg:
            assert False

        res['preload_log_list'] = result_list
        res['page_info'] = pagination

        status = True
    except Exception as e:
        print(e)
        res['msg'] = _(msg)

    res['status'] = status

    return json_response(res)


@login_required
@rights_required('client_cdn_domain_log')
def client_cdn_domain_log_list(request):
    """客户端域名日志列表"""
    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    user = request.user

    try:
        msg, result_list, pagination = get_domain_log(request, user)
        if msg:
            assert False

        res['log_list'] = result_list
        res['page_info'] = pagination

        status = True
    except AssertionError:
        res['msg'] = _(msg)

    res['status'] = status

    return json_response(res)


@login_required
@rights_required('client_cdn_create_domain')
def client_cdn_get_cert(request):
    """客户端获取证书列表"""

    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    user_id = request.POST.get('user_id', '')

    # user_id = 93

    try:
        user_id = int_check(user_id)
        if user_id is None:
            msg = af.PARAME_ERROR
            assert False

        body = {
            'user_id': user_id,
            'status': [CertConf.CERT_SUCCESS]
        }

        api_res = APIUrl.post_link('ssl_cert_query', body)
        return_code = api_res.get('return_code', 0)

        if return_code != 0:
            assert False

        cert_list = api_res.get('cert_list', [])

        result_list = []
        for i in cert_list:
            cert_dict = {
                'create_time': i.get('create_time', ''),
                'cert_name': i.get('cert_name', ''),
                'issued_to': i.get('issued_to', '')
            }
            result_list.append(cert_dict)

        result_list = sorted(
            result_list, key=lambda x: x['create_time'], reverse=True)

        res['cert_list'] = result_list
        status = True
    except Exception as e:
        print(e)
        res['msg'] = _(msg)

    res['status'] = status

    return json_response(res)


@login_required
@rights_required('client_cdn_overview')
def client_cdn_overview_data(request):
    """客户端概览数据"""

    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    try:
        user = request.user
        domain_query = Domain.objects.filter(user=user)
        domain_list = [d.domain for d in domain_query]

        start_time, end_time = get_this_month_time()

        start_time = datetime_to_timestamp(start_time)
        end_time = datetime_to_timestamp(end_time)

        _, sum_cdn_flux, _, max_cdn, _, _, _ = get_domain_flux(
            user.id, domain_list, start_time, end_time, [])

        res = {
            'domain_count': len(domain_list),
            'sum_cdn_flux': sum_cdn_flux,
            'max_cdn': max_cdn,
        }

        status = True
    except Exception as e:
        print(e)
        res['msg'] = _(msg)

    res['status'] = status

    return json_response(res)
