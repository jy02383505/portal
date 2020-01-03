
import traceback
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


from common.feed import APIUrl
from base.models import Product, UserProfile, Domain
from common.decorators import rights_required
from common.feed import SecWafConf as sf
import json
from base.models import Provider


@login_required
@rights_required('admin_security_user_list')
def admin_sec_user_list_views(request):
    """管理员cms客户绑定关系"""
    sec_product = Product.objects.filter(code='SECURITY').first()

    res = APIUrl.post_link('user_query', {})
    user_query = res.get('user_query', {})

    cms_user_list = []
    try:
        for i in user_query:
            user_id = user_query[i].get('user_id')
            user = UserProfile.objects.filter(id=user_id).first()
            if not user:
                continue

            cms_username = user_query[i].get('cms_username', '')

            if not cms_username:
                continue

            user_info = {
                'user_id': user_id,
                'username': user_query[i].get('username'),
                'cms_username': cms_username,
                'is_sec': 0
            }

            if sec_product not in user.product_list.all():
                # user_info['is_sec'] = 1
                cms_user_list.append(user_info)
    except Exception as e:
        print(e)

    res = {
        'cms_user_list': cms_user_list
    }

    return render(request, 'safe_cdn/safe_cdn_list.html', res)


@login_required
@rights_required('admin_security_domain_list')
def admin_sec_domain_list_views(request):
    """管理员安全CDN频道列表页面"""

    sec_product = Product.objects.filter(code='SECURITY').first()

    sec_user = sec_product.user_product.all()

    body = {
        'username_list': [u.username for u in sec_user]
    }

    res = APIUrl.post_link('user_query', body)
    user_query = res.get('user_query', {})

    cms_user_list = []
    for i in user_query:
        user_info = {
            'user_id': user_query[i].get('user_id'),
            'username': user_query[i].get('username'),
            'cms_username': user_query[i].get('cms_username', ''),
        }
        cms_user_list.append(user_info)

    res = {
        'cms_user_list': cms_user_list
    }

    return render(request, 'safe_cdn/safe_channel_list.html', res)


@login_required
@rights_required('all_admin_views')
def admin_alarm_list(request):
    """管理员安全CDN频道告警"""

    res = {
    }
    return render(request, 'safe_cdn/alarm.html', res)


@login_required
@rights_required('all_admin_views')
def admin_sec_overview_views(request):
    """管理员安全CDN频道统计"""

    res = {
    }
    return render(request, 'safe_cdn/admin_sec_overview.html', res)


@login_required
@rights_required('admin_security_domain_list')
def admin_sec_domain_conf_views(request, domain_id):
    """管理员安全域名配置页面"""
    provider = 'QINGSONG'

    domain_obj = Domain.objects.filter(id=domain_id).first()

    channel = '%s://%s' % (domain_obj.protocol, domain_obj.domain)

    access_point_conf = []
    for short_name in sf.ACCESS_POINT_CONF:
        info = {
            'short_name': short_name,
        }
        info.update(sf.ACCESS_POINT_CONF[short_name])
        access_point_conf.append(info)

    body = {
        'user_id': domain_obj.user_id,
        # 'user_id': 93,
        'protocol': domain_obj.protocol,
        # 'protocol': 'http',
        'domain': domain_obj.domain,
        # 'domain': 'itestxz0034.nubesi.com',
    }

    try:
        
        rCdnInfo = APIUrl.post_link('domain_cc_conf', body)
        return_code = rCdnInfo.get('return_code', 0)
        # assert False

        if return_code != 0:
            assert False

        rBind = APIUrl.post_link('whetherBind', {'channel': channel})
        api_res = APIUrl.post_link('sync_domain_waf_conf', {'channel': channel})
        res = {}

        provider_obj = Provider.objects.filter(code=provider).first()

        if api_res[provider]['return_code'] == 0:
            status = api_res[provider]['status']

            api_res[provider]['provider_name'] = provider_obj.name
            res = {
                'domain': domain_obj,
                'status': status,
                'waf_origin': sf.WAF_ORIGIN,
                'waf_default_mode_conf': sf.WAF_DEFAULT_MODE_CONF,
                'waf_self_mode_conf': sf.WAF_SELF_MODE_CONF,
                'access_type_conf': sf.ACCESS_TYPE_CONF,
                'src_type_conf': sf.SRC_TYPE_CONF,
                'access_point_conf': access_point_conf,
                'whetherBind': rBind,
                'access_type': int(api_res[provider]['access_type']),
                'access_point_cname': api_res[provider]['access_point_cname'],

                'waf_conf': api_res[provider],
                'waf_conf_json': json.dumps(api_res[provider]),
            }
    except Exception:
        print(f'admin_sec_domain_conf_views[error.] error: {traceback.format_exc()}')
    return render(request, 'safe_cdn/configure.html', res)


@login_required
@rights_required('admin_security_domain_list')
def admin_domain_waf_create_index_views(request):
    """管理员waf开通首页"""
    res = {
    }
    return render(request, 'safe_cdn/admin_domain_waf_create_index.html', res)


@login_required
@rights_required('admin_security_domain_list')
def admin_domain_waf_register_views(request, domain_id):
    """管理员waf注册页面绑定"""
    domain_obj = Domain.objects.filter(id=domain_id).first()
    access_point_conf = []
    for short_name in sf.ACCESS_POINT_CONF:
        info = {
            'short_name': short_name,
        }
        info.update(sf.ACCESS_POINT_CONF[short_name])
        access_point_conf.append(info)

    res = {
        'domain': domain_obj,
        'access_point_conf': access_point_conf,
        'access_type_conf': sf.ACCESS_TYPE_CONF,
        'domain_waf_status': 'is_create'

    }
    # print(f'\n---domain_obj.__dict__---\n{domain_obj.__dict__}')
    # print(f'\n---res---\n{res}')
    return render(request, 'safe_cdn/configure.html', res)


@login_required
@rights_required('admin_security_domain_list')
def admin_domain_waf_conf_fail_views(request):
    """管理员waf创建失败or创建中"""
    res = {
    }
    return render(request, 'safe_cdn/admin_configure_waf_fail.html', res)


@login_required
@rights_required('admin_security_domain_list')
def admin_domain_waf_create_views(request, domain_id):

    domain_obj = Domain.objects.filter(id=domain_id).first()

    provider = 'QINGSONG'
    # access_point_conf = [{'short_name': short_name}.update(sf.ACCESS_POINT_CONF[short_name]) for short_name in sf.ACCESS_POINT_CONF]

    access_point_conf = []
    for shortName in sf.ACCESS_POINT_CONF:
        tempDict = {'short_name': shortName}

        tempDict.update(sf.ACCESS_POINT_CONF[shortName])
        access_point_conf.append(tempDict)

    res = {
        'status': 1,
        'domain': domain_obj,
        'access_point_conf': access_point_conf,
        'waf_origin': sf.WAF_ORIGIN,
        'waf_default_mode_conf': sf.WAF_DEFAULT_MODE_CONF,
        'waf_self_mode_conf': sf.WAF_SELF_MODE_CONF,
        'access_type_conf': sf.ACCESS_TYPE_CONF,
        'src_type_conf': sf.SRC_TYPE_CONF,
        'domain_waf_status': 'is_create'
    }
    # print(f'admin_domain_waf_create_views res: {res}')

    return render(request, 'safe_cdn/configure.html', res)


@login_required
@rights_required('admin_security_domain_list')
def admin_domain_waf_cdn_conf_views(request, domain_id):
    """管理员waf cdn相关配置页面"""
    domain_obj = Domain.objects.filter(id=domain_id).first()
    res = {
        'domain': domain_obj
    }
    return render(request, 'safe_cdn/admin_domain_waf_cdn_conf.html', res)


@login_required
@rights_required('admin_security_domain_list')
def admin_sec_overview_views(request, domain_id):
    """管理员安全域名配置页面"""
    domain_obj = Domain.objects.filter(id=domain_id).first()

    res = {
        'domain': domain_obj,
    }
    return render(request, 'safe_cdn/statistics.html', res)

