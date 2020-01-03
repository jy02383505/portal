
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
from django.views.decorators.http import require_POST
from django.contrib.auth import login as auth_login, authenticate

from base.functions import get_menu_tree
from base.models import UserProfile, OperateLog, PermUser
from common.functions import json_response, decrypt_to, int_check
from common.feed import AccountsFeed as af, OperateMsg as om, APIUrl


@require_POST
def login(request):
    """用户登录"""
    res = {
        'status': False,
        'msg': '',
        'menus': []
    }

    username = request.POST.get('username', '')

    password = request.POST.get('password', '')

    pl = request.POST.get('pl', '0')
    pl = int(pl)

    key = request.POST.get('csrfmiddlewaretoken', '')[:16]
    vi = request.POST.get('csrfmiddlewaretoken', '')[-16:]

    error_msg = ''
    status = False
    url = ''

    try:

        if not username:
            error_msg = af.USERNAME_EMPTY
            assert False

        if not password:
            error_msg = af.PASSWORD_EMPTY
            assert False

        dec_password = decrypt_to(password, key, vi)
        password = dec_password[:pl]

        user = UserProfile.objects.filter(username=username).first()

        if user:
            user = authenticate(username=username, password=password)

            if not user:
                error_msg = af.USER_ERROR
                assert False

            if not user.is_active:
                error_msg = af.USER_NOT_ACTIVE
                assert False

            if user.reset_password:
                redirect_url = '/base/reset_password/page/'
                return HttpResponseRedirect(redirect_url)

            auth_login(request, user)

            OperateLog.write_operate_log(
                request, om.ACCOUNTS, om.LOGIN_SYSTEM)

            menus, perm_user = get_menu_tree(user)

            res['menus'] = menus
            res['perm_user'] = perm_user

            status = True
        else:
            assert False
            error_msg = af.USER_ERROR

    except AssertionError:
        res['msg'] = _(error_msg)

    res['status'] = status
    res['url'] = url

    print(res)

    return json_response(res)


def set_user_api_status(request, user):
    """用户设置api状态"""
    msg = ''

    try:
        api_status = request.POST.get('status', '')

        api_status = int_check(api_status)
        if api_status is None:
            af.PARAME_ERROR
            assert False

        body = {
            'username': user.username,
            'status': api_status
        }

        api_res = APIUrl.post_link('set_api_status', body)
        result = api_res.get('return_code', 0)
        if result != 0:
            msg = af.SEND_ERROR
            assert False
    except AssertionError:
        pass

    return msg


def user_open_parent_api(user):
    """用户设置api状态"""
    msg = ''

    res = {}
    try:
        body = {
            'username': user.username,
        }

        api_res = APIUrl.post_link('user_open_api', body)
        result = api_res.get('return_code', 0)
        if result != 0:
            msg = af.SEND_ERROR
            assert False

        res['secret_id'] = api_res.get('secret_id', '')
        res['secret_key'] = api_res.get('secret_key', '')
        res['create_time'] = api_res.get('create_time', '')
        res['api_open'] = api_res.get('api_open', 0)

    except AssertionError:
        pass

    return msg, res


def set_user_api_remove(user):
    """用户设置api状态"""
    msg = ''

    try:
        body = {
            'username': user.username,
        }

        api_res = APIUrl.post_link('set_api_remove', body)
        result = api_res.get('return_code', 0)
        if result != 0:
            msg = af.SEND_ERROR
            assert False
    except AssertionError:
        pass

    return msg
