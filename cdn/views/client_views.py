

import datetime

from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required


from base.models import Domain
from cdn.funcions import get_cdn_type_from_name, get_effective_contract

from common.feed import CDNConf, APIUrl, CertConf
from common.decorators import rights_required
from common.functions import datetime_to_str


@login_required
@rights_required('client_cdn_overview')
def client_cdn_overview_views(request):
    """客户端总览"""
    user = request.user

    domain_query = Domain.objects.filter(user=user).order_by('-protocol')

    check_domain = []
    domain_list = []
    for i in domain_query:
        domain = i.domain
        if domain not in check_domain:
            check_domain.append(domain)
            domain_dict = {
                'id': i.id,
                'domain': i.domain
            }
            domain_list.append(domain_dict)

    contract = get_effective_contract(request.user)

    res = {
        'contract': contract,
        'domain_list': domain_list
    }

    return render(request, 'cdn/client_cdn_overview.html', res)


@login_required
@rights_required('client_cdn_domain_list')
def client_statistics_views(request):
    """客户端统计"""
    user_list = []

    user = request.user

    cdn_user = [user]

    body = {
        'username_list': [user.username],
    }

    res = APIUrl.post_link('user_query', body)
    user_query = res.get('user_query', {})

    for u in cdn_user:
        username = u.username

        domain_query = Domain.objects.filter(user=u)

        user_info = user_query.get(username, {})
        if not user_info:
            continue

        cdn_opt = user_info.get('cdn_opt', [])

        check_domain = []
        domain_list = []
        for i in domain_query:
            domain_dict = {
                'id': i.id,
                'domain': i.domain,
            }
            if i.domain not in check_domain:
                domain_list.append(domain_dict)
                check_domain.append(i.domain)

        user_dict = {
            'id': u.id,
            'username': u.username,
            'domain_list': domain_list,
            'cdn_opt': cdn_opt
        }
        user_list.append(user_dict)

    res = {
        'user_list': user_list,
    }
    return render(request, 'cdn/admin_statistics.html', res)


@login_required
@rights_required('client_cdn_domain_refresh')
def client_refresh_views(request):
    """客户端刷新页面"""
    res = {
        'refresh_status': CDNConf.REFRESH_STATUS,
        'refresh_type': CDNConf.REFRESH_TYPE
    }
    return render(request, 'cdn/admin_refresh.html', res)


@login_required
@rights_required('client_cdn_domain_preload')
def client_preload_views(request):
    """管理员预热页面"""
    res = {
        'preload_status': CDNConf.PRELOAD_STATUS,
    }
    return render(request, 'cdn/admin_refresh.html', res)


@login_required
@rights_required('client_cdn_domain_log')
def client_log_download_views(request):
    """管理员日志下载"""

    user = request.user

    user_list = []
    domain_list = Domain.objects.filter(user=user)

    user_domain_list = []
    for d in domain_list:
        if d.domain not in user_domain_list:
            user_domain_list.append(d.domain)

    user_dict = {
        'id': user.id,
        'username': user.username,
        'domain_list': user_domain_list
    }
    user_list.append(user_dict)

    res = {
        'domain_list': user_domain_list
    }
    return render(request, 'cdn/admin_log_upload.html', res)


@login_required
@rights_required('client_cdn_domain_list')
def client_get_domain_list_views(request):
    """客户端查看域名列表"""

    protocol_type = [
        {'id': 'http', 'name': 'HTTP'},
        {'id': 'https', 'name': 'HTTPS'}
    ]

    cdn_type_view = [
        {'id': 'web', 'name': _('页面加速'), 'check_name': '网页'},
        {'id': 'download', 'name': _('下载加速'), 'check_name': '下载'},
        {'id': 'vod', 'name': _('点播加速'), 'check_name': '点播'},
    ]

    domain_status_views = [
        {'id': [1, 3, 5, 6, 7], 'name': _('配置中')},
        {'id': [2], 'name': _('已启动')},
        {'id': [4], 'name': _('已关闭')},
        {'id': [-1], 'name': _('下发失败')},
    ]

    contract = get_effective_contract(request.user)

    res = {
        'protocol_type': protocol_type,
        'cdn_type': cdn_type_view,
        'domain_status': domain_status_views,
        'contract': contract

    }
    return render(request, 'cdn/admin_get_domain_list.html', res)


@login_required
@rights_required('client_cdn_create_domain')
def client_cdn_create_domain_views(request):
    """客户端创建加速域名页面"""
    user = request.user
    body = {
        'username_list': [request.user.username]
    }

    res = APIUrl.post_link('user_query', body)
    user_query = res.get('user_query', {})

    username = user.username

    user_info = user_query.get(username, {})

    contract = user_info.get('contract', {})

    contract_name = ''
    product_cdn_type = []

    now = datetime_to_str(datetime.datetime.now(), _format='%Y-%m-%d')

    for c in contract:

        start_time = contract[c]['start_time']
        end_time = contract[c]['end_time']


        if start_time < now < end_time:
            product_list = contract[c]['product']
            for p in product_list:
                product_name = p['product_name']

                if CDNConf.NOVA_TYPE in product_name:
                    product_cdn_type = CDNConf.NOVA_TYPE_LIST
                    continue

                p_cdn_type = get_cdn_type_from_name(product_name)
                product_cdn_type.append(p_cdn_type)

            contract_name = c

            break
    product_cdn_type = list(set(product_cdn_type))

    user_cdn_type = []

    for ct in CDNConf.CDN_TYPE:
        ct_id = ct['id']
        if ct_id in product_cdn_type:
            user_cdn_type.append(ct)

    cms_username = user_info.get('cms_username', '')

    user_dict = {
        'id': user.id,
        'username': username,
        'cms_username': cms_username,
        'user_cdn_type': user_cdn_type,
        'contract_name': contract_name,
    }

    res = {
        'user_list': user_dict,
        'cdn_type': CDNConf.CDN_TYPE,
        'protocol_type': CDNConf.PROTOCOL_TYPE,
        'src_type': CDNConf.SRC_TYPE,
        'src_back_type': CDNConf.SRC_BACK_TYPE,
        'cache_type': CDNConf.CACHE_TYPE,
        'default_cache': CDNConf.DEFAULT_CACHE
    }
    return render(request, 'cdn/admin_cdn_create_domain.html', res)


@login_required
@rights_required('client_cdn_domain_list')
def client_cdn_edit_domain_views(request, domain_id):
    """客户端修改域名配置"""
    provider = 'CC'
    domain_obj = Domain.objects.filter(id=domain_id).first()

    res = {}
    if domain_obj:
        user_id = domain_obj.user_id

        try:
            body = {
                'user_id': user_id,
                'status': [CertConf.CERT_SUCCESS],
            }

            api_res = APIUrl.post_link('ssl_cert_query', body)
            return_code = api_res.get('return_code', 0)

            if return_code != 0:
                assert False

            cert_info_list = api_res.get('cert_list', [])

            cert_name_list = []
            for cert in cert_info_list:
                cert_name_list.append(cert.get('cert_name', ''))

            body = {
                'user_id': user_id,
                'protocol': domain_obj.protocol,
                'domain': domain_obj.domain,
                'provider': provider
            }

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

            domain_obj.cert_info = domain_conf.get('cert_info', {})

            res['domain'] = domain_obj
            res['src_type'] = CDNConf.SRC_TYPE
            res['src_back_type'] = CDNConf.SRC_BACK_TYPE
            res['cache_type'] = CDNConf.CACHE_TYPE
            res['cert_status'] = CertConf.CERT_STATUS
            res['cert_from'] = CertConf.CERT_FROM
            res['cert_list'] = cert_name_list
        except AssertionError:
            pass

    return render(request, 'cdn/modify_admin_domain_configure.html', res)

