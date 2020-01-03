
import json
import copy
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
                              handle_request_user, handle_list, handle_req_time)

from base.models import Domain, UserProfile, Product, OperateLog
from cdn.ajax.base_ajax import (get_domain_flux, get_domain_request,
                                get_domain_status_code, get_domain_list,
                                user_domain_refresh, user_domain_refresh_status,
                                user_domain_preload, user_domain_preload_status,
                                get_domain_conf, user_domain_create,
                                get_domain_log)
from cdn.funcions import make_base_excel


@login_required
@rights_required('admin_cdn_domain_list')
def admin_get_domain_list(request):
    """管理员获取列表"""
    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    user = request.user
    domain = request.POST.get('domain', '')
    user_id = request.POST.get('user_id', '')
    cdn_type = request.POST.get('cdn_type', '')
    domain_status = request.POST.get('domain_status', '[]')

    domain_query = Domain.get_domain_query_by_user(user)

    try:
        domain_status = handle_list(domain_status, dec_int=True)

        if user_id:

            user_id = int_check(user_id)
            if user_id is None:
                msg = af.PARAM_ERROR
                assert False

            domain_query = domain_query.filter(user__id=user_id)

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
@rights_required('admin_cdn_user_list')
def admin_cdn_user_list(request):
    """cdn用户列表"""
    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    id_or_username = request.POST.get('id_or_username', '')
    cms_username = request.POST.get('cms_username', '')

    cdn_product = Product.objects.filter(code='CDN').first()

    try:

        body = {
            'username_list': [],
            'cms_username': '',
            'return_type': 'is_list',
        }

        user_query = cdn_product.user_product.all()

        if id_or_username:

            check_res = int_check(id_or_username)

            if check_res is None:
                user_query = user_query.filter(username=id_or_username)
            else:
                user_query = user_query.filter(id=check_res)

        cms_user_list = []
        if user_query:
            body['username_list'] = [user.username for user in user_query]

            if cms_username:
                body['cms_username'] = cms_username

            api_res = APIUrl.post_link('user_query', body)
            api_user_query = api_res.get('user_query', {})

            print(1111111, api_user_query)

            for i in api_user_query:
                username = i.get('username', '')
                user_id = i.get('user_id', 0)
                cms_username = i.get('cms_username', '')

                cdn_opt = i.get('cdn_opt', [])

                user_info = {
                    'user_id': user_id,
                    'username': username,
                    'cms_username': cms_username,
                    'cdn_opt': cdn_opt
                }

                cms_user_list.append(user_info)

            cms_user_list = sorted(
                cms_user_list, key=lambda x: x['user_id'], reverse=True)

        check_msg, cdn_user_list, pagination = data_pagination(
            request, cms_user_list)

        if check_msg:
            res['msg'] = check_msg
            return json_response(res)

        res['cdn_user_list'] = cdn_user_list
        res['page_info'] = pagination

        status = True

    except AssertionError:
        res['msg'] = _(msg)

    res['status'] = status

    return json_response(res)


@login_required
@rights_required('admin_cdn_user_list')
def admin_cdn_user_set_conf(request):
    """管理员设置cdn用户基本配置"""
    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    user = request.user

    user_id = request.POST.get('user_id', '')

    opt = request.POST.get('opt', '["CC"]')
    cc_cms_template_type = request.POST.get('cc_cms_template', '')
    cc_icp_check = request.POST.get('cc_icp_check', "0")
    base_cname = request.POST.get('base_cname', CDNConf.BASE_CNAME)

    # user_id = 93
    # cc_cms_template_type = 2
    # cc_icp_check = True
    # opt = ['CC']
    # base_cname = '.ns.xgslb.com'

    try:
        opt = json.loads(opt)

        user_id = int_check(user_id)
        if user_id is None:
            assert False
            msg = af.PARAME_ERROR

        cc_icp_check = int_check(cc_icp_check)
        if cc_icp_check is None:
            assert False
            msg = af.PARAME_ERROR

        cc_cms_template_type = int_check(cc_cms_template_type)
        if cc_cms_template_type is None:
            assert False
            msg = af.PARAME_ERROR

        edit_user = UserProfile.objects.filter(id=user_id).first()
        if not edit_user:
            assert False
            msg = af.USER_NOT_EXIST

        fields = {
            'cc_cms_template_type': cc_cms_template_type,
            'cc_icp_check': cc_icp_check,
            'cdn_opt': opt,
            'base_cname': base_cname
        }

        body = {
            'user_id': edit_user.id,
            'username': edit_user.username,
            'fields': fields,
        }

        res = APIUrl.post_link('update_user', body)
        return_code = res.get('return_code', 0)

        if return_code != 0:
            assert False

        status = True

        log_msg = om.SET_CDN_BASE_CONF % (user.username, edit_user.username)
        OperateLog.write_operate_log(request, om.ACCOUNTS, log_msg)

    except Exception as e:
        print(e)
        res['msg'] = _(msg)

    res['status'] = status

    return json_response(res)


@login_required
@rights_required('admin_cdn_create_domain')
def admin_cdn_create_domain(request):
    """
    创建cdn域名
    """
    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }
    print(request.POST)

    opt_user = request.user

    try:
        user = handle_request_user(request)
        if not user:
            msg = af.USER_NOT_EXIST
            assert False

        msg, status = user_domain_create(request, user, opt_user)

        if not status:
            assert False

    except AssertionError:
        res['msg'] = _(msg)

    res['status'] = status

    return json_response(res)


@login_required
@rights_required('admin_cdn_create_domain')
def admin_cdn_edit_domain(request):
    """
    修改cdn域名
    """
    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    user = request.user

    user_id = request.POST.get('user_id', '')
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

        user_id = int_check(user_id)
        if user_id is None:
            msg = af.PARAME_ERROR
            assert False

        if src_back_value and not src_back_type:
            msg = af.SRC_BACK_TYPE_EMPTY
            assert False

        edit_user = UserProfile.objects.filter(id=user_id).first()
        if not edit_user:
            assert False
            msg = af.USER_NOT_EXIST

        domain_obj = Domain.objects.filter(domain=domain).first()
        if not domain_obj:
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
            'user_id': user_id,
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
        print(222222222, body)
        api_res = APIUrl.post_link('cdn_domain_edit', body)
        print(api_res)
        return_code = api_res.get('return_code', 0)

        if return_code != 0:
            assert False

        domain_obj = get_domain_conf(domain_obj)
        res['cert_info'] = domain_obj.cert_info

        status = True

        log_msg = om.EDIT_CDN_DOMAIN % (
            user.username, edit_user.username, domain)
        OperateLog.write_operate_log(request, om.ACCOUNTS, log_msg)

    except Exception as e:
        print(e)
        res['msg'] = _(msg)

    res['status'] = status

    return json_response(res)


@login_required
@rights_required('admin_cdn_create_domain')
def admin_cdn_domain_disable(request):
    """管理员域名报停"""
    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    user = request.user

    user_id = request.POST.get('user_id', '')
    domain_list = request.POST.get('domain', '[]')


    # user_id = 93
    # domain = '[itestxz0018.chinacache.com]'

    try:
        domain_list = json.loads(domain_list)

        user_id = int_check(user_id)
        if user_id is None:
            msg = af.PARAME_ERROR
            assert False

        edit_user = UserProfile.objects.filter(id=user_id).first()

        body = {
            'domain': domain_list,
            'user_id': user_id,

        }
        api_res = APIUrl.post_link('cdn_domain_disable', body)
        assert api_res
        return_code = api_res.get('return_code', 0)

        if return_code != 0:
            assert False

        status = True

        domain_str = ','.join(domain_list)
        log_msg = om.DISABLE_CDN_DOMAIN % (
            user.username, edit_user.username, domain_str)
        OperateLog.write_operate_log(request, om.ACCOUNTS, log_msg)

    except Exception as e:
        print(e)
        res['msg'] = _(msg)

    res['status'] = status

    return json_response(res)


@login_required
@rights_required('admin_cdn_create_domain')
def admin_cdn_domain_active(request):
    """管理员域名激活"""
    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    user = request.user

    user_id = request.POST.get('user_id', '')
    domain_list = request.POST.get('domain', '[]')


    # user_id = 93
    # domain = '[itestxz0018.chinacache.com]'

    domain_list = json.loads(domain_list)

    try:

        user_id = int_check(user_id)
        if user_id is None:
            msg = af.PARAME_ERROR
            assert False

        edit_user = UserProfile.objects.filter(id=user_id).first()

        body = {
            'domain': domain_list,
            'user_id': user_id,

        }
        api_res = APIUrl.post_link('cdn_domain_active', body)
        assert api_res
        return_code = api_res.get('return_code', 0)

        if return_code != 0:
            assert False

        status = True

        domain_str = ','.join(domain_list)
        log_msg = om.ACTIVE_CDN_DOMAIN % (
            user.username, edit_user.username, domain_str)
        OperateLog.write_operate_log(request, om.ACCOUNTS, log_msg)

    except Exception as e:
        print(e)
        res['msg'] = _(msg)

    res['status'] = status

    return json_response(res)


@login_required
@rights_required('admin_cdn_create_domain')
def admin_cdn_domain_conf(request):
    """
    修改cdn域名
    """
    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    user_id = request.POST.get('user_id', '')
    domain = request.POST.get('domain', '')
    provider = request.POST.get('provider', 'CC')

    # user_id = '93'
    # domain = 'itestxz0021.chinacache.com'

    user_id = int_check(user_id)

    try:

        domain_obj_list = Domain.objects.filter(domain=domain)
        if not domain_obj_list:
            assert False
            msg = af.DOMAIN_EXIST

        protocol = CDNConf.HTTP_TYPE

        for domain_obj in domain_obj_list:
            if domain_obj.protocol == CDNConf.HTTPS_TYPE:
                protocol = CDNConf.HTTPS_TYPE
                break

        user_id = int_check(user_id)
        if user_id is None:
            msg = af.PARAME_ERROR
            assert False

        body = {
            'user_id': user_id,
            'protocol': protocol,
            'domain': domain,
            'provider': provider
        }
        api_res = APIUrl.post_link('cdn_domain_sync_conf', body)
        return_code = api_res.get('return_code', 0)

        if return_code != 0:
            assert False

        res['domain_conf'] = api_res['domain_conf']

        status = True

    except Exception as e:
        print(e)
        res['msg'] = _(msg)

    res['status'] = status

    return json_response(res)


@login_required
@rights_required('admin_cdn_create_domain')
def admin_cdn_get_cert(request):
    """管理员获取证书列表"""

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
@rights_required('admin_cdn_domain_refresh')
def admin_cdn_domain_refresh(request):
    """管理员url刷新"""
    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    try:
        user = handle_request_user(request)
        if not user:
            msg = af.USER_NOT_EXIST
            assert False

        msg = user_domain_refresh(request, user)

        if msg:
            assert False

        if not msg:
            status = True
    except AssertionError:
        res['msg'] = _(msg)

    res['status'] = status

    print(res)

    return json_response(res)


@login_required
@rights_required('admin_cdn_domain_refresh')
def admin_cdn_domain_refresh_status(request):
    """管理员url刷新查询"""
    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    try:
        user = handle_request_user(request)
        if not user:
            msg = af.USER_NOT_EXIST
            assert False

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
@rights_required('admin_cdn_domain_preload')
def admin_cdn_domain_preload(request):
    """管理员url预热"""
    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    try:
        user = handle_request_user(request)
        if not user:
            msg = af.USER_NOT_EXIST
            assert False

        msg = user_domain_preload(request, user)

        if msg:
            assert False

        status = True

    except Exception as e:
        print(e)
        res['msg'] = _(msg)

    res['status'] = status
    print(res)

    return json_response(res)


@login_required
@rights_required('admin_cdn_domain_preload')
def admin_cdn_domain_preload_status(request):
    """管理员url预热查询"""
    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    try:
        user = handle_request_user(request)
        if not user:
            msg = af.USER_NOT_EXIST
            assert False

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
@rights_required('admin_cdn_domain_log')
def admin_cdn_domain_log_list(request):
    """域名日志列表"""
    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    try:
        user = handle_request_user(request)
        if not user:
            msg = af.USER_NOT_EXIST
            assert False

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
@rights_required('admin_cdn_domain_statistical')
@gzip_page
def admin_cdn_flux_data(request):
    """管理员查看计费统计数据"""

    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    start_time = request.POST.get('start_time', 0)
    end_time = request.POST.get('end_time', 0)
    user_id = request.POST.get('user_id', '')
    domain_ids = request.POST.get('domain_list', '[]')
    opts = request.POST.get('opts', '[]')

    all_flux_list = []    # 计费图表数据
    sum_cdn_flux = 0    # 总计费数据(MB)
    sum_src_flux = 0    # 总回源数据(MB)
    max_cdn = 0    # 峰值计费值(M/bps)

    table_data = []    # 每日表格数据

    try:
        user_id = int_check(user_id)
        if user_id is None:
            msg = af.PARAME_ERROR
            assert False

        msg, start_time, end_time = handle_req_time(start_time, end_time)
        if msg:
            assert False

        domain_ids = handle_list(domain_ids, dec_int=True)
        if domain_ids:
            opts = handle_list(opts)

            domain_query = Domain.objects.filter(id__in=domain_ids)
            domain_list = [i.domain for i in domain_query]

            (all_flux_list, sum_cdn_flux, sum_src_flux,
             max_cdn, max_src, table_data, opt_result) = get_domain_flux(
                user_id, domain_list, start_time, end_time, opts)

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
@rights_required('admin_cdn_domain_statistical')
@gzip_page
def admin_cdn_request_data(request):
    """管理员查看请求量统计数据"""

    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    start_time = request.POST.get('start_time', 0)
    end_time = request.POST.get('end_time', 0)
    user_id = request.POST.get('user_id', '')
    domain_ids = request.POST.get('domain_list', '[]')
    opts = request.POST.get('opts', '[]')

    request_ratio = 0    # 请求命中率(%)

    try:
        user_id = int_check(user_id)
        if user_id is None:
            msg = af.PARAME_ERROR
            assert False

        msg, start_time, end_time = handle_req_time(start_time, end_time)
        if msg:
            assert False

        domain_ids = handle_list(domain_ids, dec_int=True)
        if domain_ids:
            opts = handle_list(opts)

            domain_query = Domain.objects.filter(id__in=domain_ids)
            domain_list = [i.domain for i in domain_query]

            request_ratio = get_domain_request(
                user_id, domain_list, start_time, end_time, opts)

        status = True
    except Exception as e:
        print(e)
        res['msg'] = _(msg)


    res['status'] = status
    res['request_ratio'] = request_ratio

    return json_response(res)


@login_required
@rights_required('admin_cdn_domain_statistical')
@gzip_page
def admin_cdn_status_code_data(request):
    """管理员查看状态码统计数据"""

    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    start_time = request.POST.get('start_time', 0)
    end_time = request.POST.get('end_time', 0)
    user_id = request.POST.get('user_id', '')
    domain_ids = request.POST.get('domain_list', '[]')
    opts = request.POST.get('opts', '[]')

    all_status_code = []    # 全部状态码数据
    all_trend_result = []
    status_code_table = []
    trend_table = []
    try:
        user_id = int_check(user_id)
        if user_id is None:
            msg = af.PARAME_ERROR
            assert False

        msg, start_time, end_time = handle_req_time(start_time, end_time)
        if msg:
            assert False

        domain_ids = handle_list(domain_ids, dec_int=True)
        if domain_ids:
            opts = handle_list(opts)

            domain_query = Domain.objects.filter(id__in=domain_ids)
            domain_list = [i.domain for i in domain_query]

            (all_status_code, opt_status_code, all_trend_result,
             all_trend_data, opt_trend_data) = get_domain_status_code(
                user_id, domain_list, start_time, end_time, opts)

            all_opt_status_code = copy.deepcopy(all_status_code)
            all_opt_status_code['opt'] = 'all'
            status_code_table.append(all_opt_status_code)

            for opt in opt_status_code:
                opt_data = copy.deepcopy(opt_status_code[opt])
                opt_data['opt'] = opt
                status_code_table.append(opt_data)

                opt_ratio_data = {}
                for code in opt_status_code[opt]:
                    opt_num = opt_status_code[opt][code]
                    base_num = all_status_code.get(code, 0)

                    opt_ratio = '%.4f' % (
                    opt_num / base_num * 100 if base_num else 0)

                    opt_ratio_data[code] = opt_ratio

                opt_ratio_data['opt'] = opt
                status_code_table.append(opt_ratio_data)

            trend_table = []

            all_opt_trend_data = copy.deepcopy(all_trend_data)
            all_opt_trend_data['opt'] = 'all'
            trend_table.append(all_opt_trend_data)

            for opt in opt_trend_data:
                opt_data = copy.deepcopy(opt_trend_data[opt])
                opt_data['opt'] = opt
                trend_table.append(opt_data)

                opt_ratio_data = {}
                for code in opt_trend_data[opt]:
                    opt_num = opt_trend_data[opt][code]
                    base_num = all_trend_data.get(code, 0)

                    opt_ratio = '%.4f' % (
                    opt_num / base_num * 100 if base_num else 0)

                    opt_ratio_data[code] = opt_ratio

                opt_ratio_data['opt'] = opt
                trend_table.append(opt_ratio_data)

        status = True

    except Exception as e:
        print(e)
        res['msg'] = _(msg)

    res['all_status_code'] = all_status_code
    res['status_code_table'] = status_code_table

    res['all_trend_result'] = all_trend_result
    res['trend_table'] = trend_table

    res['status'] = status

    return json_response(res)


@login_required
@rights_required('admin_cdn_domain_statistical')
def admin_download_cdn_flux(request, start_time, end_time,
                             user_id, domain_ids, opts):
    """下载计费数据"""

    msg = ''
    status = False

    try:
        user_id = int_check(user_id)
        if user_id is None:
            msg = af.PARAME_ERROR
            assert False
        user = UserProfile.objects.filter(id=user_id).first()

        msg, start_time, end_time = handle_req_time(start_time, end_time)
        if msg:
            assert False

        domain_ids = domain_ids.split(',')
        domain_query = Domain.objects.filter(id__in=domain_ids)
        domain_list = [i.domain for i in domain_query]

        opts = opts.split(',')


        (all_flux_list, sum_cdn_flux, sum_src_flux,
         max_cdn, max_src, table_data, opt_result) = get_domain_flux(
            user_id, domain_list, start_time, end_time, opts)

        excel_name = '%s-flux_data.xls' % user.username
        sheet_name = 'Detailed Traffic Bandwidth'

        start_time = timestamp_to_str(start_time)
        end_time = timestamp_to_str(end_time)

        row, excel_path, worksheet, workbook = make_base_excel(
            excel_name, sheet_name, domain_list, start_time, end_time)

        row += 1
        worksheet.write(row, 0, label='Peak bandwidth (M/bps)')
        worksheet.write(row, 1, label=max_cdn)

        row += 1
        worksheet.write(row, 0, label='Source peak bandwidth (M/bps)')
        worksheet.write(row, 1, label=max_src)

        row += 1
        worksheet.write(row, 0, label='Total flow (MB)')
        worksheet.write(row, 1, label=sum_cdn_flux)

        row += 1
        worksheet.write(row, 0, label='Total source flow (MB)')
        worksheet.write(row, 1, label=sum_src_flux)

        row += 2
        worksheet.write(row, 0, label='Time')
        worksheet.write(row, 1, label='bandwidth (M/bps)')
        worksheet.write(row, 2, label='flow (MB)')

        base_title_row = row
        base_title_col = 3

        row += 1
        for i in all_flux_list:
            time_key = i.get('time_key', '')
            cdn_data = i.get('cdn_data', 0)

            cdn_bandwidth = cdn_data / 300 * 8

            worksheet.write(row, 0, label=time_key)
            worksheet.write(row, 1, label=cdn_bandwidth)
            worksheet.write(row, 2, label=cdn_data)

            row += 1

        for opt in opt_result:
            title_row = base_title_row

            bandwidth_title = '%s bandwidth' % opt
            bandwidth_col = base_title_col
            worksheet.write(title_row, bandwidth_col, label=bandwidth_title)

            flow_title = '%s flow' % opt
            flow_col = base_title_col + 1
            worksheet.write(title_row, flow_col, label=flow_title)

            for i in opt_result[opt]:
                title_row += 1

                cdn_data = i.get('cdn_data', 0)
                cdn_bandwidth = cdn_data / 300 * 8

                worksheet.write(title_row, bandwidth_col, label=cdn_bandwidth)
                worksheet.write(title_row, flow_col, label=cdn_data)

            base_title_col += 1

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
@rights_required('admin_cdn_domain_statistical')
def admin_download_status_code(request, start_time, end_time,
                               user_id, domain_ids, opts):
    """下载计费数据"""

    msg = ''
    status = False

    base_code = CDNConf.STATUS_CODE

    try:
        user_id = int_check(user_id)
        if user_id is None:
            msg = af.PARAME_ERROR
            assert False
        user = UserProfile.objects.filter(id=user_id).first()

        msg, start_time, end_time = handle_req_time(start_time, end_time)
        if msg:
            assert False

        domain_ids = domain_ids.split(',')
        domain_query = Domain.objects.filter(id__in=domain_ids)
        domain_list = [i.domain for i in domain_query]

        opts = opts.split(',')

        all_status_code, opt_status_code, _, _, _ = get_domain_status_code(
            user_id, domain_list, start_time, end_time, opts)

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

        opt_col = 3
        opt_list = []
        for opt in opt_status_code:
            worksheet.write(base_row, opt_col, label='{} total'.format(opt))
            worksheet.write(
                base_row, opt_col + 1, label='{} percentage'.format(opt))

            opt_list.append(opt)

            opt_col += 1

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

            col = 3
            for opt in opt_list:
                opt_num = opt_status_code[opt][code]
                worksheet.write(row, col, label=opt_num)

                opt_ratio = '%.4f' % (opt_num / num * 100 if num else 0)
                worksheet.write(row, col+1, label='{}%'.format(opt_ratio))

                col += 1

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
@rights_required('admin_cdn_domain_statistical')
def admin_download_status_code_trend(request, start_time, end_time,
                               user_id, domain_ids, opts):
    """下载计费数据"""

    msg = ''
    status = False

    base_code = CDNConf.STATUS_CODE_TREND

    try:
        user_id = int_check(user_id)
        if user_id is None:
            msg = af.PARAME_ERROR
            assert False
        user = UserProfile.objects.filter(id=user_id).first()

        msg, start_time, end_time = handle_req_time(start_time, end_time)
        if msg:
            assert False

        domain_ids = domain_ids.split(',')
        domain_query = Domain.objects.filter(id__in=domain_ids)
        domain_list = [i.domain for i in domain_query]

        opts = opts.split(',')


        _, _, _, all_trend_data, opt_trend_data = get_domain_status_code(
            user_id, domain_list, start_time, end_time, opts)

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

        opt_col = 3
        opt_list = []
        for opt in opt_trend_data:
            worksheet.write(base_row, opt_col, label='{} total'.format(opt))
            worksheet.write(
                base_row, opt_col + 1, label='{} percentage'.format(opt))

            opt_list.append(opt)

            opt_col += 1

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

            col = 3
            for opt in opt_list:
                opt_num = opt_trend_data[opt][code]
                worksheet.write(row, col, label=opt_num)

                opt_ratio = '%.4f' % (opt_num / num * 100 if num else 0)
                worksheet.write(row, col+1, label='{}%'.format(opt_ratio))

                col += 1

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