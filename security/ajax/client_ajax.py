
import os
import xlwt
import datetime
from urllib.parse import unquote, urlparse

from django.conf import settings
from django.http import StreamingHttpResponse
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required


from common.decorators import rights_required
from common.feed import (AccountsFeed as af, OperateMsg as om, APIUrl,
                         DEFAULT_RULE_CONF, WAF_ATTACK_TYPE)
from common.country_conf import COUNTRY_NAME_CONF, COUNTRY_ABBREVIATION_CONF
from common.functions import (json_response, int_check, data_pagination,
                              make_error_file, timestamp_to_str, str_to_datetime,
                              datetime_to_str)

from base.models import UserProfile, Domain, OperateLog
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
                                     user_download_rule_list)


@login_required
@rights_required('client_security_domain_list')
def parent_get_sec_domain_list(request):

    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    url = request.POST.get('domain', '')

    url_info = urlparse(url)
    protocol = url_info.scheme
    netloc = url_info.netloc
    path = url_info.path

    try:
        user = request.user

        domain_query = Domain.objects.filter(user=user)

        if url:
            if protocol and netloc:
                domain_query = domain_query.filter(
                    protocol=protocol, domain=netloc)
            else:
                domain_query = domain_query.filter(domain__contains=path)

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

            # waf标记
            is_waf = 0
            waf_info = domain_info.get('waf', [])
            if waf_info:
                is_waf = 1

            domain_dict = {
                'username': user.username,
                'WAF': is_waf,
                'domain_id': domain_obj.id,
                'channel_name': url
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
                    print(f'parent_get_sec_domain_list[get_domain_status api error.] channel: {url}')

            domain_dict_list.append(domain_dict)

        check_msg, domain_dict_list, pagination = data_pagination(
            request, domain_dict_list)

        if check_msg:
            res['msg'] = _(check_msg)
            return json_response(res)

        res['domain_list'] = domain_dict_list
        res['page_info'] = pagination

        status = True

    except Exception as e:
        res['msg'] = e

    res['status'] = status

    return json_response(res)


@login_required
@rights_required('client_security_domain_list')
def parent_get_waf_base_conf(request):
    """父账号获取waf基本配置"""

    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    provider = 'QINGSONG'

    domain_id = request.POST.get('domain_id', '')

    try:
        if not domain_id:
            msg = af.DOMAIN_NOT_EXIST
            assert False

        domain_obj = Domain.objects.filter(id=domain_id).first()
        if not domain_obj:
            msg = af.DOMAIN_NOT_EXIST
            assert False

        body = {
            'channel': '%s://%s' % (domain_obj.protocol, domain_obj.domain),
        }
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

            res['base_conf'] = base_conf

            status = True

    except AssertionError:
        res['msg'] = _(msg)

    res['status'] = status

    return json_response(res)


@login_required
@rights_required('client_security_domain_list')
def parent_set_defense_mode(request):
    """父账号自己设置规则防御模式"""
    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    provider = 'QINGSONG'

    domain_id = request.POST.get('domain_id', '')

    default_waf_mode = request.POST.get('default_waf_mode', '')
    self_waf_mode = request.POST.get('self_waf_mode', '')

    try:
        domain_obj = Domain.objects.filter(id=domain_id).first()
        if not domain_obj:
            msg = af.DOMAIN_NOT_EXIST
            assert False

        body = {
            'channel': '%s://%s' % (domain_obj.protocol, domain_obj.domain),
        }

        if default_waf_mode:
            default_waf_mode = int_check(default_waf_mode)
            if default_waf_mode is None:
                msg = af.PARAME_ERROR
                assert False

            body['default'] = 1
            body['switch'] = default_waf_mode
            log_msg = om.SET_DEFAULT_RULE_MODE % (
                request.user.username, domain_obj.domain, default_waf_mode)

        elif self_waf_mode:
            self_waf_mode = int_check(self_waf_mode)
            if self_waf_mode is None:
                msg = af.PARAME_ERROR
                assert False

            body['default'] = 0
            body['switch'] = self_waf_mode

            log_msg = om.SET_SELF_RULE_MODE % (
                request.user.username, domain_obj.domain, self_waf_mode)

        api_res = APIUrl.post_link('set_defense_mode', body)
        if api_res[provider]['return_code'] == 0:
            status = True

            OperateLog.write_operate_log(request, om.SECURITY, log_msg)

    except AssertionError:
        res['msg'] = _(msg)

    res['status'] = status

    return json_response(res)


@login_required
@rights_required('client_security_domain_list')
def parent_get_waf_default_rule(request):
    """父账号获取默认规则"""
    return user_get_waf_default_rule(request)


@login_required
@rights_required('client_security_domain_list')
def parent_get_waf_self_rule(request):
    """父账号获取自定义规则"""
    return user_get_waf_self_rule(request)


@login_required
@rights_required('client_security_domain_list')
def parent_reset_default_rule(request):
    """父账号自己设置全部默认规则开关"""
    return user_reset_default_rule(request)


@login_required
@rights_required('client_security_domain_list')
def parent_enable_default_rule(request):
    """父账号自己设置默认规则"""
    return user_enable_default_rule(request)


@login_required
@rights_required('client_security_domain_list')
def parent_enable_self_rule(request):
    """父账号自己设置自定义规则"""
    return user_enable_self_rule(request)


@login_required
@rights_required('client_security_domain_list')
def parent_get_log_list(request):
    """父账号自己查看日志"""
    return user_get_log_list(request)


@login_required
@rights_required('client_security_domain_list')
def parent_get_log_detail(request):
    """父账号查看日志详情"""

    return user_get_log_detail(request)


@login_required
@rights_required('client_security_domain_list')
def parent_download_log(request, domain_id, atk_ip,
                        start_time, end_time, log_rows):
    """父账号下载日志
    {'action': 'waf_report', 'message': 'success',
    'data': {'cur_page': 70, 'log_rows': 1381, 'waf_log': [], 'page_cnt': 70},
    'return_code': 0}
    """
    return user_download_log(request, domain_id, atk_ip,
                             start_time, end_time, log_rows)


@login_required
@rights_required('client_security_domain_list')
def parent_get_waf_statistics(request):
    """父账号查看统计数据"""
    return user_get_waf_statistics(request)


@login_required
@rights_required('client_security_domain_list')
def parent_download_time_cnt(request, domain_id, start_time, end_time):
    """父账号下载拦截攻击次数excel"""
    return user_download_time_cnt(request, domain_id, start_time, end_time)


@login_required
@rights_required('client_security_domain_list')
def parent_download_ip_list(request, domain_id, start_time, end_time):
    """父账号下载拦截攻击来源"""
    return user_download_ip_list(request, domain_id, start_time, end_time)


@login_required
@rights_required('client_security_domain_list')
def parent_download_rule_list(request, domain_id, start_time, end_time):
    """父账号下载攻击方式"""
    return user_download_rule_list(request, domain_id, start_time, end_time)
