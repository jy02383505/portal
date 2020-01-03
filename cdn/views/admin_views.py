
import datetime

from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required


from common.feed import CDNConf, APIUrl, CertConf
from base.models import (GroupProfile, UserProfile, Provider,
                         Product, Domain)
from common.decorators import rights_required
from common.functions import datetime_to_str
from base.functions import handle_perm
from cdn.ajax.base_ajax import get_domain_conf
from cdn.funcions import get_cdn_type_from_name
from common.fusion_api.cc_api import ChinaCacheAPI


@login_required
@rights_required('admin_cdn_domain_list')
def admin_cdn_user_list_views(request):
    """管理员CDN用户列表"""
    res = {
        'opt_type': CDNConf.OPT_CONF
    }
    return render(request, 'cdn/admin_cdn_user_list.html', res)


@login_required
@rights_required('admin_cdn_domain_list')
def admin_cdn_edit_domain_views(request, domain_id):
    """管理员修改域名配置"""

    res = {}

    body = {
        'status': [CertConf.CERT_SUCCESS],
    }

    api_res = APIUrl.post_link('ssl_cert_query', body)
    return_code = api_res.get('return_code', 0)

    cert_name_list = []
    if return_code == 0:
        cert_info_list = api_res.get('cert_list', [])
        for cert in cert_info_list:
            cert_name_list.append(cert.get('cert_name', ''))

    domain_obj = Domain.objects.filter(id=domain_id).first()
    if domain_obj:
        domain_obj = get_domain_conf(domain_obj)

    res['domain'] = domain_obj
    res['src_type'] = CDNConf.SRC_TYPE
    res['src_back_type'] = CDNConf.SRC_BACK_TYPE
    res['cache_type'] = CDNConf.CACHE_TYPE
    res['cert_status'] = CertConf.CERT_STATUS
    res['cert_from'] = CertConf.CERT_FROM
    res['cert_list'] = cert_name_list

    return render(request, 'cdn/modify_admin_domain_configure.html', res)


@login_required
@rights_required('admin_cdn_domain_statistical')
def admin_statistics_views(request):
    """管理员统计"""
    cdn_product = Product.objects.filter(code='CDN').first()

    cdn_user = cdn_product.user_product.all()
    user_list = []

    body = {
        'username_list': [u.username for u in cdn_user],
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

    provider_query = Provider.objects.all()
    provider_info = []
    for i in provider_query:
        provider_dict = {
            'id': i.code,
            'name': i.name
        }
        provider_info.append(provider_dict)

    res = {
        'user_list': user_list,
        'provider_info': provider_info
    }

    return render(request, 'cdn/admin_statistics.html', res)


@login_required
@rights_required('admin_cdn_domain_refresh')
def admin_refresh_views(request):
    """管理员刷新页面"""
    cdn_product = Product.objects.filter(code='CDN').first()
    cdn_user = cdn_product.user_product.all()

    user_list = []
    for i in cdn_user:
        user_dict = {
            'id': i.id,
            'username': i.username
        }
        user_list.append(user_dict)

    res = {
        'user_list': user_list,
        'refresh_status': CDNConf.REFRESH_STATUS,
        'refresh_type': CDNConf.REFRESH_TYPE
    }
    return render(request, 'cdn/admin_refresh.html', res)


@login_required
@rights_required('admin_cdn_domain_preload')
def admin_preload_views(request):
    """管理员预热页面"""
    cdn_product = Product.objects.filter(code='CDN').first()
    cdn_user = cdn_product.user_product.all()

    user_list = []
    for i in cdn_user:
        user_dict = {
            'id': i.id,
            'username': i.username
        }
        user_list.append(user_dict)

    res = {
        'user_list': user_list,
        'preload_status': CDNConf.PRELOAD_STATUS,
    }
    return render(request, 'cdn/admin_refresh.html', res)


@login_required
@rights_required('admin_cdn_domain_log')
def admin_log_download_views(request):
    """管理员日志下载"""
    cdn_product = Product.objects.filter(code='CDN').first()
    cdn_user = cdn_product.user_product.all()

    user_list = []
    for i in cdn_user:
        domain_list = Domain.objects.filter(user=i)

        user_domain_list = []
        for d in domain_list:
            if d.domain not in user_domain_list:
                user_domain_list.append(d.domain)

        user_dict = {
            'id': i.id,
            'username': i.username,
            'domain_list': user_domain_list
        }
        user_list.append(user_dict)
    res = {
        'user_list': user_list
    }
    return render(request, 'cdn/admin_log_upload.html', res)


@login_required
@rights_required('admin_cdn_domain_list')
def admin_get_domain_list_views(request):
    """管理员查看域名列表"""

    cdn_product = Product.objects.filter(code='CDN').first()

    cdn_user = cdn_product.user_product.all()
    user_list = []
    for u in cdn_user:
        user_dict = {
            'id': u.id,
            'username': u.username,
        }
        user_list.append(user_dict)

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

    res = {
        'user_list': user_list,
        'protocol_type': protocol_type,
        'cdn_type': cdn_type_view,
        'domain_status': domain_status_views
    }

    return render(request, 'cdn/admin_get_domain_list.html', res)


@login_required
@rights_required('admin_cdn_domain_list')
def admin_cdn_base_conf_views(request, user_id):
    """管理员配置cdn基础信息配置页面"""
    edit_user = UserProfile.objects.filter(id=user_id).first()
    username = edit_user.username

    body = {
        'username_list': [username]
    }

    res = APIUrl.post_link('user_query', body)
    user_query = res.get('user_query', {})

    edit_user.opt_name = []
    edit_user.template_name = ''
    edit_user.cc_icp_check = False

    try:
        cdn_opt = user_query[username]['cdn_opt']
        cc_cms_template_type = user_query[username]['cc_cms_template_type']
        cc_cms_template_type = int(cc_cms_template_type)
        cc_icp_check = user_query[username]['cc_icp_check']

        opt_name = []
        for i in cdn_opt:
            for j in CDNConf.OPT_CONF:
                if j['id'] == i:
                    opt_name.append(j['name'])

        template_name = ''
        for i in CDNConf.CMS_ANA_TEMPLATE:
            if i['id'] == cc_cms_template_type:
                template_name = i['name']
                break

        edit_user.cc_cms_template_type = cc_cms_template_type
        edit_user.opt_name = opt_name
        edit_user.template_name = template_name
        edit_user.cc_icp_check = True if cc_icp_check else False

    except Exception as e:
        print(e)

    print(edit_user.opt_name)
    print(edit_user.template_name)
    print(edit_user.cc_icp_check)

    res = {
        'edit_user': edit_user,
        'opt_conf': CDNConf.OPT_CONF,
        'cms_ana_template': CDNConf.CMS_ANA_TEMPLATE
    }
    return render(request, 'cdn/admin_cdn_base_conf.html', res)


@login_required
@rights_required('admin_cdn_create_domain')
def admin_cdn_create_domain_views(request):
    """管理员创建加速域名页面"""
    cdn_product = Product.objects.filter(code='CDN').first()

    cdn_user = cdn_product.user_product.all()

    body = {
        'username_list': [u.username for u in cdn_user]
    }

    res = APIUrl.post_link('user_query', body)
    user_query = res.get('user_query', {})
    # print(user_query)

    now = datetime_to_str(datetime.datetime.now(), _format='%Y-%m-%d')

    user_list = []
    for u in cdn_user:

        username = u.username

        user_info = user_query.get(username, {})

        contract = user_info.get('contract', {})

        if not user_info or not contract:
            continue

        contract_name = ''
        product_cdn_type = []

        for c in contract:

            start_time = contract[c]['start_time']
            end_time = contract[c]['end_time']


            if start_time <= now <= end_time:
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

        if not contract_name:
            continue

        product_cdn_type = list(set(product_cdn_type))

        user_cdn_type = []

        for ct in CDNConf.CDN_TYPE:
            ct_id = ct['id']
            if ct_id in product_cdn_type:
                user_cdn_type.append(ct)

        cms_username = user_info.get('cms_username', '')

        user_dict = {

            'id': u.id,
            'username': username,
            'cms_username': cms_username,
            'user_cdn_type': user_cdn_type,
            'contract_name': contract_name,
        }
        user_list.append(user_dict)

    res = {
        'user_list': user_list,
        'cdn_type': CDNConf.CDN_TYPE,
        'protocol_type': CDNConf.PROTOCOL_TYPE,
        'src_type': CDNConf.SRC_TYPE,
        'src_back_type': CDNConf.SRC_BACK_TYPE,
        'cache_type': CDNConf.CACHE_TYPE,
        'default_cache': CDNConf.DEFAULT_CACHE
    }
    return render(request, 'cdn/admin_cdn_create_domain.html', res)

