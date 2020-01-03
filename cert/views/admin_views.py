import copy
from django.utils.translation import ugettext as _
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


from common.feed import AccountsFeed as af, APIUrl, CertConf, CDNConf
from base.models import GroupProfile, UserProfile, Provider
from common.decorators import rights_required
from base.functions import handle_perm, int_check
from common.functions import timestamp_to_str


@login_required
@rights_required('admin_cdn_cert_manage')
def admin_cert_ssl_manage_views(request):
    """管理端证书管理页面"""
    user_query = UserProfile.objects.filter(is_parent=True)

    user_list = []
    for u in user_query:
        user_dict = {
            'id': u.id,
            'username': u.username
        }
        user_list.append(user_dict)

    res = {
        'cert_status': CertConf.CERT_STATUS,
        'cert_from': CertConf.CERT_FROM,
        'user_list': user_list,
    }

    return render(request, 'cert/admin_cert_ssl_manage.html', res)


@login_required
@rights_required('admin_cdn_cert_manage')
def admin_cert_create_views(request):
    """管理端证书创建页面"""
    user_query = UserProfile.objects.filter(is_parent=True)

    user_list = []
    for u in user_query:
        user_dict = {
            'id': u.id,
            'username': u.username
        }
        user_list.append(user_dict)

    # 过期提醒
    remind_time = [
        {'id': 0, 'name': _("不提醒")},
        {'id': 30, 'name': _("一个月")},
        {'id': 3 * 30, 'name': _("三个月")},
    ]

    res = {
        'user_list': user_list,
        'remind_time': remind_time
    }

    return render(request, 'cert/admin_cert_create.html', res)


@login_required
@rights_required('admin_cdn_cert_manage')
def admin_cert_edit_views(request, cert_name, user_id):
    """管理端证书修改页面"""

    try:
        if user_id:
            user_id = int_check(user_id)
            if user_id is None:
                msg = af.PARAME_ERROR
                assert False

        body = {
            'cert_name': cert_name,
            'user_id': user_id
        }

        api_res = APIUrl.post_link('ssl_cert_detail', body)
        return_code = api_res.get('return_code', 0)

        if return_code != 0:
            assert False

        cert_detail = api_res.get('cert_detail', {})

    except AssertionError:
        pass

    res = {
        'cert_detail': cert_detail,
        'remind_time': CertConf.REMIND_TIME
    }

    return render(request, 'cert/admin_cert_create.html', res)


@login_required
@rights_required('admin_cdn_cert_manage')
def admin_cert_detail_views(request, cert_name, user_id):
    """管理端证书详情页面"""

    cert_detail = {}

    provider_list = Provider.objects.all()

    provider_dict_list = []
    for i in provider_list:
        provider_dict = {
            'name': i.name,
            'code': i.code
        }
        provider_dict_list.append(provider_dict)

    try:
        if user_id:
            user_id = int_check(user_id)
            if user_id is None:
                msg = af.PARAME_ERROR
                assert False

        body = {
            'cert_name': cert_name,
            'user_id': user_id
        }

        api_res = APIUrl.post_link('ssl_cert_detail', body)
        return_code = api_res.get('return_code', 0)

        if return_code != 0:
            assert False

        cert_detail = api_res.get('cert_detail', {})

        relation_list = cert_detail['relation_list']

        relation_result = []
        for i in relation_list:
            domain = i.get('domain', '')
            status = i.get('status', [])

            status_list = list(set(status))

            if CDNConf.DOMAIN_SERVING in status_list:
                status_list.pop(status_list.index(CDNConf.DOMAIN_SERVING))

            if not status_list:
                status_name = CDNConf.DOMAIN_SERVING
            else:
                status_value = status_list[0]
                status_name = status_value

            result_dict = {
                'domain': domain,
                'status': status_name
            }

            relation_result.append(result_dict)

        cert_detail['relation_list'] = relation_result

        log_list = cert_detail['log_list']

        temp_list = []
        for i in log_list:
            create_time = i.get('create_time', 0)
            create_time = timestamp_to_str(create_time)
            temp_log = copy.deepcopy(i)
            temp_log['create_time'] = create_time

            opt_result_dict = i.get('opt_result')
            opt_list = []
            for p in opt_result_dict:
                temp = {'opt': p, 'result': opt_result_dict[p]}
                opt_list.append(temp)
            temp_log['opt_result'] = opt_list

            temp_list.append(temp_log)

        temp_list = sorted(
            temp_list, key=lambda x: x['create_time'], reverse=True)

        cert_detail['log_list'] = temp_list

    except AssertionError:
        pass

    res = {
        'cert_detail': cert_detail,
        'cert_status': CertConf.CERT_STATUS,
        'cert_from': CertConf.CERT_FROM,
        'domain_status': CDNConf.DOMAIN_STATUS,
        'opt_send_status': CertConf.OPT_SEND_STATUS,
        'provider_list': provider_dict_list
    }

    return render(request, 'cert/admin_cert_detail.html', res)