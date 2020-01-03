import traceback
import copy
import json
from urllib.parse import urlparse

from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required


from common.decorators import rights_required
from common.feed import (AccountsFeed as af, OperateMsg as om, APIUrl,
                         SecWafConf as sf)
from common.functions import (json_response, int_check, data_pagination, is_ip,
                              is_domain, decrypt_to, parseProtocolRecordDomain)
from base.models import (UserProfile, Domain, Provider, Product,
                         OperateLog, Strategy)
from common.fusion_api.cc_api import ChinaCacheAPI

from security.ajax.base_ajax import (user_get_waf_default_rule,
                                     user_get_waf_self_rule,
                                     user_reset_default_rule,
                                     user_enable_default_rule,
                                     user_enable_self_rule,
                                     user_get_log_list, user_download_log,
                                     user_get_log_detail,
                                     user_get_waf_statistics,
                                     user_download_time_cnt,
                                     user_download_ip_list,
                                     user_download_rule_list
                                     )


@login_required
@rights_required('admin_security_user_list')
def admin_sec_user_list(request):
    """安全用户列表"""
    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    id_or_username = request.POST.get('id_or_username', '')
    cms_username = request.POST.get('cms_username', '')

    sec_product = Product.objects.filter(code='SECURITY').first()

    try:

        body = {
            'username_list': [],
            'cms_username': '',
            'return_type': 'is_list',
        }

        user_query = sec_product.user_product.all()

        if id_or_username:

            check_res = int_check(id_or_username)

            if check_res is None:
                user_query = user_query.filter(username=id_or_username)
            else:
                user_query = user_query.filter(id=check_res)

        body['username_list'] = [user.username for user in user_query]

        if cms_username:
            body['cms_username'] = cms_username

        api_res = APIUrl.post_link('user_query', body)
        api_user_query = api_res.get('user_query', {})

        cms_user_list = []
        for i in api_user_query:
            username = i.get('username', '')
            user_id = i.get('user_id', 0)
            cms_username = i.get('cms_username', '')
            if not cms_username:
                continue

            user = user_query.filter(id=user_id).first()
            if not user:
                continue

            domain_num = Domain.objects.filter(user=user).count()

            user_info = {
                'user_id': user_id,
                'username': username,
                'cms_username': cms_username,
                'domain_num': domain_num
            }

            cms_user_list.append(user_info)

        cms_user_list = sorted(
            cms_user_list, key=lambda x: x['user_id'], reverse=True)

        check_msg, sec_user_list, pagination = data_pagination(
            request, cms_user_list)

        if check_msg:
            res['msg'] = check_msg
            return json_response(res)

        res['sec_user_list'] = sec_user_list
        res['page_info'] = pagination

        status = True

    except AssertionError:
        res['msg'] = _(msg)

    res['status'] = status

    return json_response(res)


@login_required
@rights_required('admin_add_security_user')
def admin_create_sec_user(request):
    """创建安全用户"""
    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    sec_product = Product.objects.filter(code='SECURITY').first()
    strategy = Strategy.get_obj_from_property('QINGSONG', 'SECURITY', 'WAF')

    user_ids = request.POST.getlist('user_ids[]', '')

    try:
        user_list = UserProfile.objects.filter(id__in=user_ids)

        if not user_list:
            msg = af.USER_NOT_EXIST
            assert False

        for user in user_list:
            user.product_list.add(sec_product)
            user.strategy_list.add(strategy)
            user.save()

            log_msg = om.CREATE_SECURITY_USER % (
                request.user.username, user.username)
            OperateLog.write_operate_log(
                request, om.SECURITY, log_msg)

        status = True

    except AssertionError:
        res['msg'] = _(msg)

    res['status'] = status

    return json_response(res)


@login_required
@rights_required('admin_add_security_domain')
def admin_get_cms_channel_list(request):
    """管理员获取cms频道"""

    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    cms_username = request.POST.get('cms_username', '')
    user_id = request.POST.get('user_id', '')

    try:

        user_id = int_check(user_id)

        if user_id is None:
            assert False
            msg = af.USER_NOT_EXIST

        body = {
            'user_id_list': [int(user_id)],
            'return_type': 'is_list'
        }
        api_res = APIUrl.post_link('domain_query', body)
        domain_query = api_res.get('domain_query', [])

        url_list = [
            '%s://%s' % (i['protocol'], i['domain']) for i in domain_query]

        cms_channel_list = ChinaCacheAPI.get_channel_by_cms(cms_username)

        channel_list = []
        for i in cms_channel_list:
            channel_name = i.get('channel_name', '')
            channel_info = copy.deepcopy(i)
            has_create = True if channel_name in url_list else False
            channel_info['has_create'] = has_create

            channel_list.append(channel_info)

        channel_list = sorted(
            channel_list, key=lambda x: urlparse(x['channel_name']).netloc)

        res['cms_channel_list'] = channel_list

        status = True

    except AssertionError:
        res['msg'] = _(msg)

    res['status'] = status

    return json_response(res)


@login_required
@rights_required('admin_add_security_domain')
def admin_create_sec_domain(request):
    """管理员添加安全域名"""

    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    channel_info_list = request.POST.getlist('channel_info_list', [])
    user_id = request.POST.get('user_id', '')

    channel_info_list = json.loads(channel_info_list[0])

    try:
        user_id = int_check(user_id)
        if user_id is None:
            msg = af.USER_NOT_EXIST
            assert False

        user = UserProfile.objects.filter(id=user_id).first()

        domain_info_list = []
        for channel_info in channel_info_list:

            channel_name = channel_info.get('channel_name', '')

            url_info = urlparse(channel_name)
            domain = url_info.netloc
            protocol = url_info.scheme

            domain_info = {
                'domain': domain,
                'protocol': protocol,
                'user_id': user_id,
            }
            domain_info_list.append(domain_info)

        body = {
           'domain_info_list': domain_info_list
        }

        api_res = APIUrl.post_link('domain_create', body)
        api_res = api_res.get('result_list', False)

        if api_res:
            for i in api_res:
                domain = i.get('domain', '')
                protocol = i.get('protocol', '')
                insert_flag = i.get('insert_flag', '')

                if insert_flag:
                    domain_obj, _ = Domain.objects.get_or_create(
                        domain=domain, protocol=protocol, user=user)
                    domain_obj.save()

                    url = '%s://%s' % (protocol, domain)
                    log_msg = om.CREATE_SECURITY_DOMAIN % (user.username, url)
                    OperateLog.write_operate_log(
                        request, om.SECURITY, log_msg)

            status = True

    except AssertionError:
        res['msg'] = _(msg)

    res['status'] = status

    return json_response(res)


@login_required
@rights_required('admin_security_domain_list')
def admin_get_sec_domain_list(request):
    """管理员查看安全域名"""
    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    id_or_username = request.POST.get('id_or_username', '')
    cms_username = request.POST.get('cms_username', '')
    domain = request.POST.get('domain', '')

    try:
        body = {
            'username_list': [],
            'cms_username': '',
            'return_type': 'is_dict'
        }

        sec_product = Product.objects.filter(code='SECURITY').first()
        user_query = sec_product.user_product.all()

        if id_or_username:

            check_res = int_check(id_or_username)

            if check_res is None:
                user_query = user_query.filter(username=id_or_username)
            else:
                user_query = user_query.filter(id=check_res)

        if user_query:
            body['username_list'] = [user.username for user in user_query]

        if cms_username:
            body['cms_username'] = cms_username

        user_ids = []
        api_res = APIUrl.post_link('user_query', body)
        user_info_list = api_res.get('user_query', {})

        if user_info_list:
            user_ids = [
                user_info_list[i]['user_id'] for i in user_info_list]

        domain_query = Domain.objects.filter(user_id__in=user_ids)

        if domain:
            if domain.startswith('http'):
                protocol, record, domain = parseProtocolRecordDomain(domain)
                domain = f'{record}.{domain}'
            domain_query = Domain.objects.filter(domain__contains=domain)

        domain_query = domain_query.order_by('-id')

        domain_name_list = []
        if domain_query:
            domain_name_list = [i.domain for i in domain_query]

        body = {
            'domain_list': domain_name_list
        }
        api_res = APIUrl.post_link('domain_query', body)
        api_domain_query = api_res.get('domain_query', [])

        domain_dict_list = []
        for domain_obj in domain_query:

            url = '%s://%s' % (domain_obj.protocol, domain_obj.domain)

            if url not in api_domain_query:
                continue

            domain_info = api_domain_query.get(url, {})

            user_id = domain_info.get('user_id')
            user = UserProfile.objects.filter(id=user_id).first()
            username = user.username
            cms_username = ''
            if username in user_info_list:
                cms_username = user_info_list.get(
                    username, {}).get('cms_username', '')

            # waf 服务判断
            is_waf = 0
            strategy_waf = domain_info.get('waf', [])
            if strategy_waf:
                is_waf = 1

            domain_dict = {
                'user_id': user_id,
                'username': username,
                'WAF': is_waf,
                'domain_id': domain_obj.id,
                'channel_name': url,
                'cms_username': cms_username
            }
            if is_waf:
                #---get domain status info.
                '''
                    0：显示“开通waf”
                    1：显示“待审核”
                    2：显示“审核不通过”
                    3：显示“配置”+“统计”
                '''
                status_from_api = APIUrl.post_link('get_domain_status', {'channel': url})
                if status_from_api['return_code'] == 0:
                    channel_status = status_from_api['data'].get('status', 0)
                    domain_dict['WAF'] = channel_status
                else:
                    print(f'admin_get_sec_domain_list[get_domain_status api error.] channel: {url}')

            domain_dict_list.append(domain_dict)

        check_msg, domain_dict_list, pagination = data_pagination(
            request, domain_dict_list)

        if check_msg:
            res['msg'] = _(check_msg)
            return json_response(res)

        res['domain_list'] = domain_dict_list
        res['page_info'] = pagination

        status = True

    except Exception:
        print(traceback.format_exc())

    res['status'] = status

    return json_response(res)


@login_required
@rights_required('admin_security_domain_list')
def admin_check_domain_waf_status(request):
    """管理员检查安全域名在青松状态"""
    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }
    provider = 'QINGSONG'
    domain_id = request.POST.get('domain_id', '')

    try:

        domain_obj = Domain.objects.filter(id=domain_id).first()
        if not domain_obj:
            msg = af.DOMAIN_NOT_EXIST
            assert False

        body = {
            'channel': '%s://%s' % (domain_obj.protocol, domain_obj.domain),
            'provider': provider
        }
        api_res = APIUrl.post_link('check_waf_status', body)
        message = api_res[provider].get('message', 'success')
        msg = '' if message == 'success' else message
        print(api_res)

        if api_res[provider].get('return_code', 1) == 0:

            check_status = api_res[provider]['status']

            waf_switch = 0
            check_result = ''
            status_msg = ''
            if check_status == 0:
                check_result = 'is_binding'
                waf_switch = 1
            elif check_status == 1:
                check_result = 'is_binding'

            elif check_status == 2:
                check_result = 'is_create'

            elif check_status == 3:
                status_msg = _(sf.DOMAIN_WAIT_AUDIT)
                check_result = 'is_auditing'
                msg = status_msg

            elif check_status == 4:
                status_msg = _(sf.DOMAIN_AUDIT_FAILED)
                check_result = 'is_audit_failed'
                msg = status_msg
            else:
                status_msg = _(sf.DOMAIN_CHECK_FAILED)
                check_result = 'is_check_failed'
                msg = status_msg

            res['check_result'] = check_result
            res['waf_switch'] = waf_switch
            res['status_msg'] = status_msg
            res['msg'] = msg
            status = True
        elif api_res[provider].get('return_code', 1) == -1:
            msg = sf.WAF_TOKEN_EMPTY
            assert False

    except Exception as e:
        print(e)
        res['msg'] = _(msg)

    res['msg'] = msg
    res['status'] = status

    print(res)

    return json_response(res)


@login_required
@rights_required('admin_security_domain_list')
def admin_domain_waf_binding(request):
    """管理员绑定waf域名"""
    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    provider = 'QINGSONG'

    domain_id = request.POST.get('domain_id', '')
    access_type = request.POST.get('access_type', '2')
    short_name = request.POST.get('short_name', '')

    # domain_id = 8
    # short_name = 'GZ'

    try:
        if short_name not in sf.ACCESS_POINT_CONF:
            msg = af.PARAME_ERROR
            assert False

        access_point = sf.ACCESS_POINT_CONF[short_name]['name']
        access_point_cname = sf.ACCESS_POINT_CONF[short_name]['cname']

        domain_obj = Domain.objects.filter(id=domain_id).first()
        if not domain_obj:
            msg = af.DOMAIN_NOT_EXIST
            assert False
        domain = domain_obj.domain

        body = {
            'provider': provider,
            'domain': domain,
            'access_type': access_type,
            'access_point': access_point,
            'access_point_cname': access_point_cname,
            'confirm_cdn_preload': True,
            'confirm_cdn_http_layered': True,
            'confirm_cdn_https_layered': True,
            'short_name': short_name
        }
        api_res = APIUrl.post_link('waf_binding', body)
        message = api_res.get('message', 'success')
        msg = '' if message == 'success' else message

        if api_res['return_code'] == 0:

            res['status'] = ''
            status = True

            log_msg = om.BINDING_WAF_DOMAIN % (request.user.username, domain)
            OperateLog.write_operate_log(
                request, om.SECURITY, log_msg)

    except AssertionError:
        res['msg'] = _(msg)

    res['msg'] = msg
    res['status'] = status

    return json_response(res)


@login_required
@rights_required('admin_security_domain_list')
def admin_domain_waf_create(request):
    """管理员创建waf域名"""
    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    provider = 'QINGSONG'

    domain_id = request.POST.get('domain_id', '')
    access_type = request.POST.get('access_type', '2')
    short_name = request.POST.get('short_name', '')

    src_type = request.POST.get('src_type', '2')
    src_address = request.POST.get('src_address', '')
    src_port = request.POST.get('src_port', '')
    src_host = request.POST.get('src_host', '')
    ssl_status = request.POST.get('ssl_status', False)
    cert_id = request.POST.get('cert_id', '')
    default_waf_mode = request.POST.get('default_waf_mode', '')
    self_waf_mode = request.POST.get('self_waf_mode', '')

    # domain_id = 8
    # short_name = 'GZ'
    print(f'admin_domain_waf_create request.POST: {request.POST}')

    try:
        if short_name not in sf.ACCESS_POINT_CONF:
            msg = af.PARAME_ERROR
            assert False

        access_point = sf.ACCESS_POINT_CONF[short_name]['name']
        access_point_cname = sf.ACCESS_POINT_CONF[short_name]['cname']

        domain_obj = Domain.objects.filter(id=domain_id).first()
        if not domain_obj:
            msg = af.DOMAIN_NOT_EXIST
            assert False
        domain = domain_obj.domain

        body = {
            'channel': f'{domain_obj.protocol}://{domain}',
            'provider': provider,

            'domain': domain,
            'short_name': short_name,
            'access_type': access_type,
            'access_point': access_point,
            'access_point_cname': access_point_cname,
            'src_type': src_type,
            'src_address': src_address,
            'src_port': src_port,
            'ssl_status': ssl_status,
            'cert_id': cert_id,
            'default_waf_mode': default_waf_mode,
            'self_waf_mode': self_waf_mode,

            # 'confirm_cdn_preload': True,
            # 'confirm_cdn_http_layered': True,
            # 'confirm_cdn_https_layered': True,
        }
        api_res = APIUrl.post_link('waf_create', body)
        message = api_res['message']
        msg = '' if message == 'success' else message

        if api_res['return_code'] == 0:

            res['status'] = ''
            status = api_res['status']

            log_msg = om.CREATE_WAF_DOMAIN % (request.user.username, domain)
            OperateLog.write_operate_log(
                request, om.SECURITY, log_msg)

    except AssertionError:
        res['msg'] = _(msg)

    res['msg'] = msg
    res['status'] = status
    print(f'\n---res---\n{res}')

    return json_response(res)


@login_required
@rights_required('admin_security_domain_list')
def admin_sync_domain_waf_conf(request):
    """管理员同步域名waf配置信息"""

    msg = ''
    status = False

    provider = 'QINGSONG'

    res = {
        'status': status,
        'msg': msg
    }

    domain_id = request.POST.get('domain_id', '')

    # domain_id = 8

    try:
        domain_obj = Domain.objects.filter(id=domain_id).first()
        if not domain_obj:
            msg = af.DOMAIN_NOT_EXIST
            assert False

        channel = '%s://%s' % (domain_obj.protocol, domain_obj.domain)

        body = {
            'channel': channel,
        }
        api_res = APIUrl.post_link('sync_domain_waf_conf', body)
        message = api_res[provider].get('message', 'success')
        msg = '' if message == 'success' else message

        if api_res[provider]['return_code'] == 0:
            """
            {
                'domain': 'itest.chinacache.com',
                'access_type': '2',
                'access_point': '广州',
                'access_point_cname': 'cc-waf-gz.ccgslb.com.cn',
                'confirm_cdn_preload': True,
                'confirm_cdn_http_layered': True,
                'confirm_cdn_https_layered': True,
                'status': 4,
                'source_is_ip': True,
                'source_addr': '223.202.202.15',
                'port': '80',
                'ssl_status': 1,
                'cert_id': '333330',
                'return_code': 0,
                'cert_name': 'mzr_delete_final_1_2211',
                'default_waf_mode': 2,
                'self_waf_mode': 1
            }
            """
            waf_conf = api_res[provider]
            provider_obj = Provider.objects.filter(code=provider).first()

            waf_conf['provider_name'] = provider_obj.name
            waf_conf['provider_name'] = provider_obj.name

            res['waf_conf'] = waf_conf
            status = True

    except Exception as e:
        print(traceback.format_exc())
        res['msg'] = _(msg)

    res['msg'] = msg
    res['status'] = status

    return json_response(res)


@login_required
@rights_required('admin_security_domain_list')
def admin_set_domain_waf_conf(request):
    """管理员设置waf 基本配置

    update = {
        'domain': '域名',
        'access_point': '接入点',
        'access_point_cname': '接入点对应cname',
        'access_type': 'waf接入方式 目前是 2',
        'src_type': '1 ip回源 & 2 域名回源',
        'src_address': '回源值 域名回源就是域名,ip回源就是ip',
        'src_port': '回源端口',
        'src_host': '回源host',
        'ssl_status': '是否启用https',
        'cert_name': '证书名称',
        'default_waf_mode': '默认规则防御模式',
        'self_waf_mode': '自定义规则防御模式',
    }

    """

    msg = ''
    status = False

    provider = 'QINGSONG'

    res = {
        'status': status,
        'msg': msg
    }

    domain_id = request.POST.get('domain_id', '')
    short_name = request.POST.get('short_name', '')

    access_type = request.POST.get('access_type', '2')
    src_type = request.POST.get('src_type', '2')
    src_address = request.POST.get('src_address', '')
    src_port = request.POST.get('src_port', '')
    src_host = request.POST.get('src_host', '')
    ssl_status = request.POST.get('ssl_status', False)
    cert_id = request.POST.get('cert_id', '')
    default_waf_mode = request.POST.get('default_waf_mode', '')
    self_waf_mode = request.POST.get('self_waf_mode', '')

    # domain_id = 8

    # short_name = 'GZ'
    # default_waf_mode = 3
    # self_waf_mode = 0

    try:
        domain_obj = Domain.objects.filter(id=domain_id).first()
        if not domain_obj:
            msg = af.DOMAIN_NOT_EXIST
            assert False

        domain = domain_obj.domain
        channel = '%s://%s' % (domain_obj.protocol, domain)

        body = {
            'channel': channel,
            'access_type': access_type,
        }

        if short_name:
            access_point = sf.ACCESS_POINT_CONF[short_name]['name']
            access_point_cname = sf.ACCESS_POINT_CONF[short_name]['cname']
            body['access_point'] = access_point
            body['access_point_cname'] = access_point_cname

        if src_address and src_type:
            src_type = int_check(src_type)
            if src_type is None:
                msg = af.PARAME_ERROR
                assert False

            if src_type == sf.SRC_TYPE_IP:
                if not is_ip(src_address):
                    msg = af.PARAME_ERROR
                    assert False
            elif src_type == sf.SRC_TYPE_DOMAIN:
                if not is_domain(src_address):
                    msg = af.PARAME_ERROR

            body['src_type'] = src_type
            body['src_address'] = src_address

        if src_port:
            body['src_port'] = src_port

        if src_host:
            body['src_host'] = src_host

        if default_waf_mode:
            body['default_waf_mode'] = default_waf_mode
        if self_waf_mode:
            body['self_waf_mode'] = self_waf_mode

        if ssl_status:
            body['ssl_status'] = ssl_status

        if cert_id:
            body['cert_id'] = cert_id

        api_res = APIUrl.post_link('set_domain_waf_conf', body)

        if api_res[provider]['return_code'] == 0:
            status = True

            log_msg = om.EDIT_WAF_CONF % (request.user.username, domain)
            OperateLog.write_operate_log(
                request, om.SECURITY, log_msg)

    except Exception as e:
        print(e)
        res['msg'] = _(msg)

    res['status'] = status

    return json_response(res)


@login_required
@rights_required('admin_security_domain_list')
def admin_upload_waf_cert(request):
    """管理员上传证书"""

    msg = ''
    status = False

    provider = 'QINGSONG'

    res = {
        'status': status,
        'msg': msg
    }

    domain_id = request.POST.get('domain_id', '')
    name = request.POST.get('name', '')

    key = request.POST.get('csrfmiddlewaretoken', '')[:16]
    vi = request.POST.get('csrfmiddlewaretoken', '')[-16:]

    cert_value = request.POST.get('cert_value', '')
    dec_cert_value = decrypt_to(cert_value, key, vi)
    cert_pl = request.POST.get('cert_pl', '0')

    key_value = request.POST.get('key_value', '')
    dec_key_value = decrypt_to(key_value, key, vi)
    key_pl = request.POST.get('key_pl', '0')
    try:
        if not name:
            msg = af.CERT_NAME_EMPTY
            assert False

        cert_pl = int_check(cert_pl)
        if cert_pl is None:
            msg = af.PARAME_ERROR
            assert False

        key_pl = int_check(key_pl)
        if key_pl is None:
            msg = af.PARAME_ERROR
            assert False

        cert_value = dec_cert_value[:cert_pl]
        key_value = dec_key_value[:key_pl]

        domain_obj = Domain.objects.filter(id=domain_id).first()
        if not domain_obj:
            msg = af.DOMAIN_NOT_EXIST
            assert False

        domain = domain_obj.domain
        channel = '%s://%s' % (domain_obj.protocol, domain)

        body = {
            'channel': channel,
            'name': name,
            'cert': cert_value,
            'key': key_value
        }
        api_res = APIUrl.post_link('waf_cert_upload', body)
        msg = api_res[provider]['message']

        if api_res[provider]['return_code'] == 0:
            status = True
            cert_id = api_res[provider].get('data', {}).get('cert_id', '')
            res['cert_id'] = cert_id

            log_msg = om.UPLOAD_WAF_CERT % (request.user.username, name)
            OperateLog.write_operate_log(
                request, om.SECURITY, log_msg)
        res['msg'] = _(msg)

    except Exception as e:
        print(traceback.format_exc())
        res['msg'] = _(msg)

    res['status'] = status

    return json_response(res)


@login_required
@rights_required('admin_security_domain_list')
def admin_domain_waf_set_cdn(request):
    """管理员设置cdn"""

    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    domain_id = request.POST.get('domain_id', '')
    switch = request.POST.get('switch', '')
    confirm_cdn_preload = request.POST.get('confirm_cdn_preload', 0)
    confirm_cdn_http_layered = request.POST.get('confirm_cdn_http_layered', 0)
    confirm_cdn_https_layered = request.POST.get('confirm_cdn_https_layered', 0)

    # domain_id = 8
    # switch = 0
    # confirm_cdn_preload = 1
    # confirm_cdn_http_layered = 1
    # confirm_cdn_https_layered = 1

    try:
        domain_obj = Domain.objects.filter(id=domain_id).first()
        if not domain_obj:
            msg = af.DOMAIN_NOT_EXIST
            assert False
        domain = domain_obj.domain

        switch = int_check(switch)
        if switch is None:
            msg = af.PARAME_ERROR
            assert False

        confirm_cdn_preload = int_check(confirm_cdn_preload)
        if confirm_cdn_preload is None:
            msg = af.PARAME_ERROR
            assert False

        confirm_cdn_http_layered = int_check(confirm_cdn_http_layered)
        if confirm_cdn_http_layered is None:
            msg = af.PARAME_ERROR
            assert False

        confirm_cdn_https_layered = int_check(confirm_cdn_https_layered)
        if confirm_cdn_https_layered is None:
            msg = af.PARAME_ERROR
            assert False

        body = {
            'domain': domain,
            'switch': switch,
            'confirm_cdn_preload': True if confirm_cdn_preload else False,
            'confirm_cdn_http_layered': True if confirm_cdn_http_layered
            else False,
            'confirm_cdn_https_layered': True if confirm_cdn_https_layered
            else False,

        }
        api_res = APIUrl.post_link('domain_waf_set_cdn', body)

        if api_res['return_code'] == 0:
            status = True
            switch_name = '开启' if switch else '关闭'
            log_msg = om.SET_WAF_CDN_STATUS % (
                request.user.username, domain, switch_name)
            OperateLog.write_operate_log(
                request, om.SECURITY, log_msg)

    except AssertionError:
        res['msg'] = _(msg)

    res['status'] = status

    return json_response(res)


@login_required
@rights_required('admin_security_domain_list')
def admin_domain_set_waf(request):
    """管理员启用waf"""

    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }
    provider = 'QINGSONG'

    domain_id = request.POST.get('domain_id', '')
    switch = request.POST.get('switch', '')

    try:
        domain_obj = Domain.objects.filter(id=domain_id).first()
        if not domain_obj:
            msg = af.DOMAIN_NOT_EXIST
            assert False
        domain = domain_obj.domain

        switch = int_check(switch)
        if switch is None:
            msg = af.PARAME_ERROR
            assert False

        body = {
            'channel': '%s://%s' % (domain_obj.protocol, domain),
            "switch": switch
        }
        api_res = APIUrl.post_link('domain_waf_opt_waf', body)
        message = api_res[provider].get('message', 'success')
        msg = '' if message == 'success' else message

        if api_res[provider]['return_code'] == 0:
            status = True

            switch_name = '开启' if switch else '关闭'
            log_msg = om.SET_WAF_STATUS % (
                request.user.username, domain, switch_name)
            OperateLog.write_operate_log(
                request, om.SECURITY, log_msg)

    except Exception as e:
        print(traceback.format_exc())
        res['msg'] = _(msg)

    res['msg'] = msg
    res['status'] = status

    return json_response(res)


@login_required
@rights_required('admin_security_domain_list')
def admin_domain_del_waf(request):
    """管理员删除waf"""

    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }
    provider = 'QINGSONG'

    domain_id = request.POST.get('domain_id', '')

    try:
        domain_obj = Domain.objects.filter(id=domain_id).first()
        if not domain_obj:
            msg = af.DOMAIN_NOT_EXIST
            assert False
        domain = domain_obj.domain

        body = {
            'channel': '%s://%s' % (domain_obj.protocol, domain),
        }
        api_res = APIUrl.post_link('domain_del_waf', body)
        message = api_res[provider].get('message', 'success')
        msg = '' if message == 'success' else message

        if api_res[provider]['return_code'] == 0:
            status = True

            log_msg = om.SET_WAF_STATUS % (
                request.user.username, domain, '删除waf')
            OperateLog.write_operate_log(
                request, om.SECURITY, log_msg)

    except Exception as e:
        print(traceback.format_exc())
        res['msg'] = _(msg)

    res['msg'] = msg
    res['status'] = status

    return json_response(res)


@login_required
@rights_required('admin_security_domain_list')
def admin_get_waf_default_rule(request):
    """管理员获取waf默认规则"""
    return user_get_waf_default_rule(request)


@login_required
@rights_required('admin_security_domain_list')
def admin_get_waf_self_rule(request):
    """管理员获取自定义规则"""
    return user_get_waf_self_rule(request)


@login_required
@rights_required('admin_security_domain_list')
def admin_reset_default_rule(request):
    """管理员自己设置全部默认规则开关"""
    return user_reset_default_rule(request)


@login_required
@rights_required('admin_security_domain_list')
def admin_enable_default_rule(request):
    """管理员自己设置默认规则"""
    return user_enable_default_rule(request)


@login_required
@rights_required('admin_security_domain_list')
def admin_enable_self_rule(request):
    """管理员自己设置自定义规则"""
    return user_enable_self_rule(request)


@login_required
@rights_required('admin_security_domain_list')
def admin_get_log_list(request):
    """管理员自己查看日志"""
    return user_get_log_list(request)


@login_required
@rights_required('admin_security_domain_list')
def admin_get_log_detail(request):
    """管理员查看日志详情"""

    return user_get_log_detail(request)


@login_required
@rights_required('admin_security_domain_list')
def admin_download_log(request, domain_id, atk_ip,
                       start_time, end_time, log_rows):
    """管理员下载日志
    {'action': 'waf_report', 'message': 'success',
    'data': {'cur_page': 70, 'log_rows': 1381, 'waf_log': [], 'page_cnt': 70},
    'return_code': 0}
    """
    return user_download_log(request, domain_id, atk_ip,
                             start_time, end_time, log_rows)


@login_required
@rights_required('admin_security_domain_list')
def admin_get_waf_statistics(request):
    """管理员查看统计数据"""
    return user_get_waf_statistics(request)


@login_required
@rights_required('admin_security_domain_list')
def admin_download_time_cnt(request, domain_id, start_time, end_time):
    """管理员下载拦截攻击次数excel"""
    return user_download_time_cnt(request, domain_id, start_time, end_time)


@login_required
@rights_required('admin_security_domain_list')
def admin_download_ip_list(request, domain_id, start_time, end_time):
    """管理员下载拦截攻击来源"""
    return user_download_ip_list(request, domain_id, start_time, end_time)


@login_required
@rights_required('admin_security_domain_list')
def admin_download_rule_list(request, domain_id, start_time, end_time):
    """管理员下载攻击方式"""
    return user_download_rule_list(request, domain_id, start_time, end_time)
