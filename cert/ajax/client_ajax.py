
import json
from urllib.parse import urlparse

from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required


from common.decorators import rights_required
from common.fusion_api.cc_api import ChinaCacheAPI
from common.feed import AccountsFeed as af, OperateMsg as om, APIUrl, CertConf
from common.functions import (json_response, int_check, data_pagination,
                              decrypt_to, handle_list)

from base.models import Domain, UserProfile, Product, OperateLog



@login_required
@rights_required('client_cdn_cert_manage')
def client_cert_list(request):
    """客户端证书列表"""
    msg = ''
    status = False
    user = request.user

    res = {
        'status': status,
        'msg': msg
    }

    cert_name = request.POST.get('cert_name', '')
    status = request.POST.get('status', '[]')

    # cert_name = 'xz_test_0009'
    # status = 1

    try:
        status_list = handle_list(status, dec_int=True)

        if not status_list:
            status_list = [
                CertConf.CERT_CONDUCT, CertConf.CERT_SUCCESS,
                CertConf.CERT_FAIL, CertConf.CERT_TIMEOUT,
                CertConf.CERT_UPDATE
            ]

        body = {
            'user_id': user.id,
            'status': status_list,
        }

        if cert_name:
            body['cert_name'] = cert_name

        api_res = APIUrl.post_link('ssl_cert_query', body)
        print(11111111, api_res)
        return_code = api_res.get('return_code', 0)

        if return_code != 0:
            assert False

        result_list = api_res.get('cert_list', [])

        cert_list = []
        for cert_info in result_list:

            # cert_info['cert_from'] = CertConf.cert_from_name(
            #     cert_info['cert_from'])
            #
            # cert_info['status'] = CertConf.cert_status_name(
            #     cert_info['status'])

            cert_list.append(cert_info)

        result_list = sorted(
            cert_list, key=lambda x: x['create_time'], reverse=True)

        check_msg, result_list, pagination = data_pagination(
            request, result_list)

        if check_msg:
            res['msg'] = check_msg
            return json_response(res)

        res['cert_list'] = result_list
        res['page_info'] = pagination

        status = True
    except Exception as e:
        print(e)
        res['msg'] = _(msg)

    res['status'] = status

    print(res)

    return json_response(res)


@login_required
@rights_required('client_cdn_cert_manage')
def client_cert_create_or_edit(request):
    """客户端证书上传与修改"""
    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    user = request.user

    cert_name = request.POST.get('cert_name', '')
    remark = request.POST.get('remark', '')
    email = request.POST.get('email', '')
    cert_from = request.POST.get('cert_from', 0)
    period = request.POST.get('period', 0)
    is_update = request.POST.get('is_update', 0)

    key = request.POST.get('csrfmiddlewaretoken', '')[:16]
    vi = request.POST.get('csrfmiddlewaretoken', '')[-16:]

    cert_value = request.POST.get('cert_value', '')
    dec_cert_value = decrypt_to(cert_value, key, vi)
    cert_pl = request.POST.get('cert_pl', '0')

    key_value = request.POST.get('key_value', '')
    dec_key_value = decrypt_to(key_value, key, vi)
    key_pl = request.POST.get('key_pl', '0')


    # cert_name = 'xz_test_0009'
    # username = 'xz_test'
    # remark = '备注备注'
    # email = 'zheng.xiang@chinacahce.com'
    # cert_value = '--------字符串省略'
    # key_value = '--------字符串省略'
    # cert_from = 0
    # period = 0
    # is_update = 0


    try:
        if not cert_name:
            msg = af.CERT_NAME_EMPTY
            assert False

        if not email:
            msg = af.CERT_EMAIL_EMPTY
            assert False

        if period:
            period = int_check(period)
            if period is None:
                msg = af.PARAME_ERROR
                assert False

        if cert_from:
            cert_from = int_check(cert_from)
            if cert_from is None:
                msg = af.PARAME_ERROR
                assert False

        if is_update:
            is_update = int_check(is_update)
            if is_update is None:
                msg = af.PARAME_ERROR
                assert False

        if not cert_value or not cert_value:
            msg = af.CERT_VALUE_OR_KEY_EMPTY
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


        body = {
            'cert_name': cert_name,
            'username': user.username,
            'remark': remark,
            'email': email,
            'cert_value': cert_value,
            'key_value': key_value,
            'cert_from': cert_from,
            'period': period,
            'is_update': is_update,
            'opt_username': request.user.username
        }

        print(11111111111, body)


        api_res = APIUrl.post_link('ssl_cert_create_or_edit', body)
        return_code = api_res.get('return_code', 0)

        print(2222222222, api_res)

        if return_code != 0:
            res['msg'] = api_res.get('err_msg', '')
            assert False

        status = True
    except Exception as e:
        print(e)
        res['msg'] = _(msg)

    res['status'] = status

    return json_response(res)


@login_required
@rights_required('client_cdn_cert_manage')
def client_cert_delete(request):
    """客户端证书删除"""
    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    user = request.user

    cert_name = request.POST.get('cert_name', '')

    # cert_name = 'xz_test_0009'

    try:

        body = {
            'cert_name': cert_name,
            'user_id': user.id
        }

        api_res = APIUrl.post_link('ssl_cert_delete', body)
        assert api_res

        return_code = api_res.get('return_code', 0)

        if return_code != 0:
            msg = api_res.get('err_msg', '')
            assert False

        status = True
    except Exception as e:
        print(e)
        res['msg'] = _(msg)

    res['status'] = status

    return json_response(res)