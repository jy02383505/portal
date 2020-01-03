
from django.contrib.auth.models import Group
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required

from common.decorators import rights_required
from common.feed import AccountsFeed as af, OperateMsg as om
from base.functions import create_user, get_user_perm_strategy_list
from common.functions import json_response, int_check, data_pagination
from base.models import (UserProfile, OperateLog, GroupProfile, PermStrategy,
                         Perm, UserPermStrategy)

from base.ajax.base_ajax import (set_user_api_status, user_open_parent_api,
                                 set_user_api_remove)


@login_required
def client_reset_password(request):
    """子账号重置密码"""
    user = request.user

    password = request.POST.get('password', '').strip()
    msg = ''

    user.set_password(password)
    user.reset_password = False
    user.save()
    status = True
    res = {
        'status': status,
        'msg': msg
    }

    return json_response(res)


@login_required
@rights_required('child_manage')
def parent_get_child_list(request):
    """父账号查看子账号列表"""
    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    user = request.user

    username = request.POST.get('username', '').strip()

    check_filter = {
        'parent_username': user.username
    }

    if username:
        check_filter['username'] = username

    user_list = UserProfile.objects.filter(**check_filter)

    check_msg, user_list, pagination = data_pagination(request, user_list)

    if check_msg:
        res['msg'] = _(check_msg)
        return json_response(res)

    user_dict_list = []

    for u in user_list:

        user_perm_strategy = UserPermStrategy.objects.filter(user=u).first()

        user_perm_strategy_dict_list = []

        if user_perm_strategy:
            for i in user_perm_strategy.perm_strategy.all():
                perm_strategy_dict = {
                    'id': i.id,
                    'name': i.name,
                    'remark': i.remark
                }
                user_perm_strategy_dict_list.append(perm_strategy_dict)

        user_dict = {
            'id': u.id,
            'username': u.username,
            'create_time': str(u.date_joined)[:19],
            'remark': u.remark,
            'user_perm_strategy': user_perm_strategy_dict_list
        }
        user_dict_list.append(user_dict)

    status = True

    res['status'] = status
    res['user_list'] = user_dict_list
    res['page_info'] = pagination

    return json_response(res)


@login_required
@rights_required('child_create')
def create_child_user(request):
    """创建子账号号用户"""
    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    is_api = request.POST.get('is_api', 0)
    reset_password = request.POST.get('reset_password', 0)
    email = request.POST.get('email', '')
    mobile = request.POST.get('mobile', '')
    remark = request.POST.get('remark', '')

    perm_strategy_ids = request.POST.getlist('perm_strategy[]', '')

    try:

        if not username:
            msg = af.USERNAME_EMPTY
            assert False

        check_user = UserProfile.objects.filter(username=username)
        if check_user:
            msg = af.USER_EXIST
            assert False

        if not password:
            msg = af.PASSWORD_EMPTY
            assert False

        is_api = int_check(is_api)
        if is_api is None:
            msg = af.PARAM_ERROR
            assert False

        reset_password = int_check(reset_password)
        if reset_password is None:
            msg = af.PARAM_ERROR
            assert False

    except AssertionError:
        res['msg'] = _(msg)
        return json_response(res)

    if is_api:
        print('给api通信')

    identity = 'is_child'

    group = Group.objects.filter(id=GroupProfile.CUSTOMER_CHILD_ID).first()

    creator_username = request.user.username

    param = {
        'username': username,
        'password': password,
        'group': group,
        'identity': identity,
        'email': email,
        'mobile': mobile,
        'remark': remark,
        'reset_password': True if reset_password else False,
        'creator_username': creator_username
    }

    user = create_user(**param)
    if not user:
        res['msg'] = _(af.PARAM_ERROR)
        return json_response(res)

    UserPermStrategy.assign_perm(perm_strategy_ids, user)

    log_msg = om.CREATE_USER % (creator_username, identity, username)
    OperateLog.write_operate_log(request, om.ACCOUNTS, log_msg)

    status = True

    res['status'] = status

    return json_response(res)


@login_required
@rights_required('child_create')
def edit_child_user(request):
    """修改子账号"""

    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    obj_id = request.POST.get('obj_id', 0)
    password = request.POST.get('password', '')
    is_api = request.POST.get('is_api', '')
    reset_password = request.POST.get('reset_password', '')
    email = request.POST.get('email', '')
    mobile = request.POST.get('mobile', '')
    remark = request.POST.get('remark', '')
    is_active = request.POST.get('is_active', '')

    perm_strategy_ids = request.POST.getlist('perm_strategy[]', '')

    try:

        check_user = UserProfile.objects.filter(id=obj_id).first()
        if not check_user:
            msg = af.USER_NOT_EXIST
            assert False

        if is_api:
            is_api = int_check(is_api)
            if is_api is None:
                msg = af.PARAM_ERROR
                assert False

            # TODO 通信api 实现key的删除

        if reset_password:
            reset_password = int_check(reset_password)
            if reset_password is None:
                msg = af.PARAM_ERROR
                assert False

            check_user.reset_password = True if reset_password else False

        if is_active:
            is_active = int_check(is_active)
            if is_api is None:
                msg = af.PARAM_ERROR
                assert False
            check_user.is_active = True if is_active else False

    except AssertionError:
        res['msg'] = _(msg)
        return json_response(res)

    if email:
        check_user.email = email
    if mobile:
        check_user.mobile = mobile
    if remark:
        check_user.remark = remark

    if password:
        check_user.set_password(password)

    check_user.save()

    if perm_strategy_ids:
        user_perm = UserPermStrategy.objects.filter(user=check_user).first()
        user_perm.perm_strategy.clear()
        UserPermStrategy.assign_perm(perm_strategy_ids, check_user)

    log_msg = om.EDIT_USER % (request.user.username, check_user.username)
    OperateLog.write_operate_log(request, om.ACCOUNTS, log_msg)

    status = True

    res['status'] = status

    return json_response(res)


@login_required
@rights_required('perm_strategy_create')
def create_perm_strategy(request):
    """父账号创建权限策略"""
    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    name = request.POST.get('name', '')
    remark = request.POST.get('remark', '')

    creator_username = request.user.username

    perm_list = request.POST.getlist('perm[]', '')

    try:
        if not name:
            msg = af.PERM_STRATEGY_NAME_EMPTY
            assert False

        if not perm_list:
            msg = af.PERM_LIST_EMPTY
            assert False

        parameter = {
            'name': name,
            'remark': remark,
            'creator_username': creator_username,
            'strategy_type': PermStrategy.PARENT_NUM
        }

        perm_strategy = PermStrategy(**parameter)
        perm_strategy.save()

        perm_list = Perm.objects.filter(code__in=perm_list)
        for perm in perm_list:
            perm_strategy.perm.add(perm)

    except AssertionError:
        res['msg'] = _(msg)
        return json_response(res)

    log_msg = om.CREATE_PERM_STRATEGY % (
        creator_username, name, perm_strategy.id)
    OperateLog.write_operate_log(request, om.ACCOUNTS, log_msg)

    status = True

    res['status'] = status

    return json_response(res)


@login_required
@rights_required('perm_strategy_create')
def edit_perm_strategy(request):
    """修改权限策略"""

    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    obj_id = request.POST.get('obj_id', '')

    name = request.POST.get('name', '')
    remark = request.POST.get('remark', '')

    creator_username = request.user.username

    perm_list = request.POST.getlist('perm[]', '')

    try:
        if not name:
            msg = af.PERM_STRATEGY_NAME_EMPTY
            assert False

        if not perm_list:
            msg = af.PERM_LIST_EMPTY
            assert False

        perm_strategy = PermStrategy.objects.filter(id=obj_id).first()

        if not perm_strategy:
            msg = af.PERM_STRATEGY_NOT_EXIST
            assert False

        if name:
            perm_strategy.name = name

        if remark:
            perm_strategy.remark = remark

        if perm_list:

            perm_strategy.perm.clear()

            perm_list = Perm.objects.filter(code__in=perm_list)
            for perm in perm_list:
                perm_strategy.perm.add(perm)

    except AssertionError:
        res['msg'] = _(msg)
        return json_response(res)

    log_msg = om.EDIT_PERM_STRATEGY % (creator_username, name, perm_strategy.id)
    OperateLog.write_operate_log(request, om.ACCOUNTS, log_msg)

    status = True

    res['status'] = status

    return json_response(res)


@login_required
@rights_required('perm_strategy_create')
def delete_perm_strategy(request):
    """父账号删除权限策略"""
    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    obj_id = request.POST.get('obj_id', '')

    creator_username = request.user.username

    try:
        perm_strategy = PermStrategy.objects.filter(
            id=obj_id, creator_username=creator_username).first()

        if not perm_strategy:
            msg = af.PERM_STRATEGY_NOT_EXIST
            assert False

        perm_strategy.delete()

    except AssertionError:
        res['msg'] = _(msg)
        return json_response(res)

    log_msg = om.DELETE_PERM_STRATEGY % (
        creator_username, perm_strategy.name, perm_strategy.id)
    OperateLog.write_operate_log(request, om.ACCOUNTS, log_msg)

    status = True

    res['status'] = status

    return json_response(res)


@login_required
@rights_required('access_manage_menu')
def parent_get_perm_strategy_list(request):
    """父账号获取权限策略列表"""
    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    msg, perm_strategy_dict_list = get_user_perm_strategy_list(request)

    if msg:
        res['msg'] = _(msg)
        return json_response(res)

    status = True
    res['status'] = status
    res['perm_strategy_list'] = perm_strategy_dict_list

    return json_response(res)


@login_required
@rights_required('client_api_info')
def client_open_parent_api(request):
    """客户端开启用户api功能"""
    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }
    user = request.user

    try:
        msg, api_res = user_open_parent_api(user)

        if not msg:
            api_info = list()

            api_info_dict = {
                'secret_id': api_res.get('secret_id', ''),
                'secret_key': api_res.get('secret_key', ''),
                'create_time': api_res.get('create_time', ''),
                'status': api_res.get('api_open', ''),
                'type': _(af.COMMON)
            }
            api_info.append(api_info_dict)
            res['api_info'] = api_info

            log_msg = om.OPEN_API % (user.username, user.username)
            OperateLog.write_operate_log(request, om.ACCOUNTS, log_msg)

            status = True

    except AssertionError:
        res['msg'] = _(msg)

    res['status'] = status
    print(res)

    return json_response(res)


@login_required
@rights_required('client_api_info')
def client_set_parent_api_status(request):
    """客户端设置api状态"""
    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }
    user = request.user

    try:
        msg = set_user_api_status(request, user)
        if msg:
            assert False

        log_msg = om.OPEN_SET_API_STATUS % (user.username, user.username)
        OperateLog.write_operate_log(request, om.ACCOUNTS, log_msg)

        status = True

    except AssertionError:
        res['msg'] = _(msg)

    res['status'] = status

    return json_response(res)


@login_required
@rights_required('client_api_info')
def client_set_parent_api_remove(request):
    """客户端开启用户api功能"""
    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }
    user = request.user

    try:
        msg = set_user_api_remove(user)

        if not msg:
            log_msg = om.REMOVE_API % (user.username, user.username)
            OperateLog.write_operate_log(request, om.ACCOUNTS, log_msg)

            status = True

    except AssertionError:
        res['msg'] = _(msg)

    res['status'] = status
    print(res)

    return json_response(res)
