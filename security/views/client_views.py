
from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required

from base.models import Domain
from common.decorators import rights_required
from common.feed import SecWafConf as sf
from common.feed import APIUrl


@login_required
@rights_required('client_security_domain_list')
def parent_sec_domain_conf_views(request, domain_id):
    """父账号安全域名配置页面"""

    domain_obj = Domain.objects.filter(id=domain_id).first()

    waf_default_mode_conf = [
        {'id': 0, 'cname': _('关闭')},
        {'id': 1, 'cname': _('普通模式')},
        {'id': 2, 'cname': _('严防模式')},
        {'id': 3, 'cname': _('观察模式')},
    ]

    waf_self_mode_conf = [
        {'id': 0, 'cname': _('关闭')},
        {'id': 1, 'cname': _('普通模式')},
    ]

    body = {
        'channel': '%s://%s' % (domain_obj.protocol, domain_obj.domain),
    }
    provider = 'QINGSONG'
    api_res = APIUrl.post_link('get_waf_base_info', body)

    if api_res[provider]['return_code'] == 0:
        api_res = api_res[provider]
        try:
            default_waf_mode = int(api_res.get('default_waf_mode', 0))
        except Exception as e:
            print(e)
            default_waf_mode = 0

        try:
            self_waf_mode = int(api_res.get('self_waf_mode', 0))
        except Exception as e:
            print(e)
            self_waf_mode = 0

        base_conf = {
            'is_https': int(api_res.get('is_https', False)),
            'default_waf_mode': default_waf_mode,
            'self_waf_mode': self_waf_mode
        }

    res = {
        'domain': domain_obj,
        'base_conf': base_conf,
        'waf_default_mode_conf': waf_default_mode_conf,
        'waf_self_mode_conf': waf_self_mode_conf
    }

    return render(request, 'safe_cdn/configure.html', res)


@login_required
@rights_required('client_security_domain_list')
def parent_sec_domain_list_views(request):
    """父账号安全域名配置页面"""
    res = {
    }
    return render(request, 'safe_cdn/safe_channel_list.html', res)


@login_required
@rights_required('client_security_domain_list')
def parent_sec_overview_views(request, domain_id):
    """父账号安全域名配置页面"""
    domain_obj = Domain.objects.filter(id=domain_id).first()

    res = {
        'domain': domain_obj,
    }
    return render(request, 'safe_cdn/statistics.html', res)

