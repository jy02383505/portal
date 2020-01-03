
from django.db.models import Q
from django.contrib.auth.models import Group
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, authenticate

from base.functions import create_user, get_menu_tree

from common.decorators import rights_required
from common.feed import AccountsFeed as af, OperateMsg as om
from common.functions import (json_response, decrypt_to, authorize, int_check,
                              PAGE_SIZE, get_pagination, timestamp_to_datetime,
                              data_pagination)

from base.models import (UserProfile, OperateLog, GroupProfile, PermUser,
                         PermGroup)


@require_POST
def login(request):
    """用户登录`
    优先校验本地mysql
    本地没有用户校验ldap系统
    """
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

            # cc 用户ldap登录
            if user.is_staff:
                login_flag, msg = authorize(username, password)
                if not login_flag:
                    error_msg = af.USER_ERROR
                    assert False

                user.set_password(password)
                user.save()

                user = authenticate(username=username, password=password)

                auth_login(request, user)
                OperateLog.write_operate_log(
                    request, om.ACCOUNTS, om.LOGIN_LDAP_SYSTEM)

            # 系统内置账号登录
            else:
                user = authenticate(username=username, password=password)
                if user:
                    if not user.is_active:
                        error_msg = af.USER_NOT_ACTIVE
                        assert False

                auth_login(request, user)

                OperateLog.write_operate_log(
                    request, om.ACCOUNTS, om.LOGIN_SYSTEM)

            menus = get_menu_tree(user)

            res['menus'] = menus
            status = True
        else:
            assert False
            error_msg = af.USER_ERROR

    except AssertionError:
        res['msg'] = error_msg

    res['status'] = status

    return json_response(res)


@login_required
@rights_required('parent_create')
def create_parent_user(request):
    """创建父账号用户"""
    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    company = request.POST.get('company', '')
    user_type = request.POST.get('user_type', '')
    linkman = request.POST.get('linkman', '')
    email = request.POST.get('email', '')
    mobile = request.POST.get('mobile', '')

    perm_list = request.POST.getlist('perm[]', '')

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

        if not company:
            msg = af.COMPANY_EMPTY
            assert False

    except AssertionError:
        res['msg'] = msg
        return json_response(res)

    identity = user_type

    group = Group.objects.filter(id=GroupProfile.CUSTOMER_ID)

    creator_username = request.user.username

    param = {
        'username': username,
        'password': password,
        'group': group,
        'identity': identity,
        'company': company,
        'linkman': linkman,
        'email': email,
        'mobile': mobile,
        'creator_username': creator_username

    }

    user = create_user(**param)

    if not user:
        res['msg'] = af.PARAM_ERROR
        return json_response(res)

    if perm_list:
        for perm_id in perm_list:
            PermUser.assign_perm(perm_id, user)

    log_msg = om.CREATE_USER % (creator_username, identity, username)
    OperateLog.write_operate_log(request, om.ACCOUNTS, log_msg)

    status = True

    res['status'] = status

    return json_response(res)


@login_required
@rights_required('parent_create')
def edit_parent_user(request):
    """修改父账号用户"""
    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    username = request.POST.get('username', '')
    company = request.POST.get('company', '')
    user_type = request.POST.get('user_type', '')
    linkman = request.POST.get('linkman', '')
    email = request.POST.get('email', '')
    mobile = request.POST.get('mobile', '')

    is_active = request.POST.get('is_active', '0')

    perm_list = request.POST.getlist('perm[]', '')

    try:

        check_user = UserProfile.objects.filter(username=username)
        if not check_user:
            msg = af.USER_NOT_EXIST
            assert False

        is_active = int_check(is_active)
        if is_active is None:
            msg = af.PARAME_ERROR
            assert False

        check_user.is_active = True if is_active else False

    except AssertionError:
        res['msg'] = msg
        return json_response(res)

    creator_username = request.user.username

    if company:
        check_user.company = company

    if user_type == 'is_parent':
        check_user.is_parent = True
        check_user.is_agent = False
    if user_type == 'is_agent':
        check_user.is_parent = False
        check_user.is_agent = True

    if linkman:
        check_user.linkman = linkman
    if email:
        check_user.email = email
    if mobile:
        check_user.mobile = mobile

    if perm_list:
        user_perm = PermUser.objects.filter(user=check_user)
        user_perm.delete()

        for perm_id in perm_list:
            PermUser.assign_perm(perm_id, check_user)

    check_user.save()

    log_msg = om.EDIT_USER % (creator_username, username)
    OperateLog.write_operate_log(request, om.ACCOUNTS, log_msg)

    status = True

    res['status'] = status

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
        res['msg'] = msg
        return json_response(res)

    if is_api:
        print('给api通信')

    identity = 'is_child'

    group = Group.objects.filter(id=GroupProfile.CUSTOMER_CHILD_ID)

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
        res['msg'] = af.PARAM_ERROR
        return json_response(res)

    log_msg = om.CREATE_USER % (creator_username, identity, username)
    OperateLog.write_operate_log(request, om.ACCOUNTS, log_msg)

    status = True

    res['status'] = status

    return json_response(res)


@login_required
@rights_required('admin_create')
def create_admin_user(request):
    """创建管理员"""
    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }
    username = request.POST.get('username', '')

    try:

        if not username:
            msg = af.USERNAME_EMPTY
            assert False

        check_user = UserProfile.objects.filter(username=username)
        if check_user:
            msg = af.USER_EXIST
            assert False

    except AssertionError:
        res['msg'] = msg
        return json_response(res)

    password = ''    # ldap 密码使用云密码
    identity = 'is_admin'
    group = Group.objects.filter(id=GroupProfile.ADMIN_ID)
    creator_username = request.user.username

    param = {
        'username': username,
        'password': password,
        'group': group,
        'identity': identity,
        'creator_username': creator_username
    }

    user = create_user(**param)

    if not user:
        res['msg'] = af.PARAM_ERROR
        return json_response(res)

    log_msg = om.CREATE_USER % (creator_username, identity, username)
    OperateLog.write_operate_log(request, om.ACCOUNTS, log_msg)

    status = True

    res['status'] = status

    return json_response(res)


@login_required
@rights_required('admin_create')
def edit_admin_user(request):
    """修改管理员账号用户"""
    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    username = request.POST.get('username', '')
    group_id = request.POST.get('group_id', '')
    is_active = request.POST.get('is_active', '0')

    try:

        if not username:
            msg = af.USERNAME_EMPTY
            assert False

        check_user = UserProfile.objects.filter(username=username)
        if not check_user:
            msg = af.USER_NOT_EXIST
            assert False

        is_active = int_check(is_active)
        if is_active is None:
            msg = af.PARAME_ERROR
            assert False

        group = Group.objects.filter(id=group_id).first()
        if not group:
            msg = af.GROUP_EMPTY
            assert False

        check_user.groups.clear()
        check_user.groups.add(group)

        check_user.is_active = True if is_active else False

        check_user.save()

    except AssertionError:
        res['msg'] = msg
        return json_response(res)

    creator_username = request.user.username

    log_msg = om.EDIT_USER % (creator_username, username)
    OperateLog.write_operate_log(request, om.ACCOUNTS, log_msg)

    status = True

    res['status'] = status

    return json_response(res)


def _get_user_list(request, group_ids):
    """检查获取用户列表参数"""
    msg = ''
    username = request.POST.get('username', '').strip()

    is_active = request.POST.get('is_active', '')

    check_filter = {}

    if username:
        check_filter['username'] = username

    if group_ids:
        check_filter['groups__id__in'] = group_ids

    user_list = UserProfile.objects.filter(**check_filter)

    try:
        if is_active:
            is_active = int_check(is_active)
            if is_active is None:
                msg = af.PARAME_ERROR
                assert False

            user_list = user_list.filter(is_active=is_active)
    except AssertionError:
        user_list = []

    return msg, user_list


@login_required
@rights_required('all_parent_views')
def admin_get_parent_list(request):
    """管理员获取父账号列表"""

    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    groups = Group.objects.filter(name=GroupProfile.CUSTOMER)
    group_ids = [i.id for i in groups]

    msg, user_list = _get_user_list(request, group_ids)
    if msg:
        res['msg'] = msg
        return json_response(res)

    if user_list:
        user_type = request.POST.get('user_type', '')

        if user_type == 'is_parent':
            user_list = user_list.filter(is_parent=True)
        elif user_type == 'is_agent':
            user_list = user_list.filter(is_agent=True)

    check_msg, user_list, pagination = data_pagination(request, user_list)

    if check_msg:
        res['msg'] = check_msg
        return json_response(res)

    user_dict_list = []

    for u in user_list:

        user_dict = {
            'id': u.id,
            'username': u.username,
            'user_type': u.type_name,
            'is_active': u.is_active
        }
        user_dict_list.append(user_dict)

    status = True

    res['status'] = status
    res['user_list'] = user_dict_list
    res['page_info'] = pagination

    return json_response(res)


@login_required
@rights_required('all_admin_views')
def admin_get_admin_list(request):
    """管理员获取管理员列表"""

    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    group_id = request.POST.get('group_id', '')
    if group_id:
        groups = Group.objects.filter(id=group_id)
        group_ids = [i.id for i in groups]
    else:
        admin_group = GroupProfile.group_views()
        group_ids = [i['id'] for i in admin_group]
    msg, user_list = _get_user_list(request, group_ids)
    if msg:
        res['msg'] = msg
        return json_response(res)

    check_msg, user_list, pagination = data_pagination(request, user_list)

    if check_msg:
        res['msg'] = check_msg
        return json_response(res)

    user_dict_list = []

    for u in user_list:
        user_group = u.groups.first()

        user_dict = {
            'id': u.id,
            'username': u.username,
            'group_name': user_group.name if user_group else '',
            'is_active': u.is_active
        }
        user_dict_list.append(user_dict)

    status = True

    res['status'] = status
    res['user_list'] = user_dict_list
    res['page_info'] = pagination

    return json_response(res)


def _get_opt_log_list(request, user_type):

    start_time = request.POST.get('start_time', 0)
    end_time = request.POST.get('end_time', 0)
    username = request.POST.get('username', '')

    size = request.POST.get('size', PAGE_SIZE)
    page = request.POST.get('page', '1')

    msg = ''
    pagination = None
    try:

        if start_time and end_time:
            try:
                start_time = timestamp_to_datetime(start_time)
                end_time = timestamp_to_datetime(end_time)
            except TypeError:
                msg = af.PARAME_ERROR
                assert False

        log_list = OperateLog.get_operator_logs(
            user_type=user_type, username=username,
            start_time=start_time, end_time=end_time)

        size = int_check(size)
        page = int_check(page)
        if size is None or page is None or page == 0:
            msg = af.PARAME_ERROR
            assert False

        start = (page - 1) * size
        end = page * size

        total = len(log_list)

        pagination = get_pagination(page, total, size)

        result_list = log_list[start:end]
    except AssertionError:
        result_list = []

    return msg, result_list, pagination


@login_required
@rights_required('all_parent_opt_log_views')
def admin_get_parent_opt_log_list(request):
    """管理员获取父账号操作记录列表"""

    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    user_type = 'is_parent'

    msg, log_list, pagination = _get_opt_log_list(request, user_type)

    status = True

    res['status'] = status
    res['log_list'] = log_list
    res['page_info'] = pagination

    return json_response(res)


@login_required
@rights_required('all_admin_opt_log_views')
def admin_get_admin_opt_log_list(request):
    """管理员获取管理员账号操作记录列表"""

    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    user_type = 'is_admin'

    msg, log_list, pagination = _get_opt_log_list(request, user_type)

    status = True

    res['status'] = status
    res['log_list'] = log_list
    res['page_info'] = pagination

    return json_response(res)


@login_required
@rights_required('group_manage')
def admin_get_group_list(request):
    """管理员角色列表"""
    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    # 供应商名称&资源包名称&资源包ID
    info = request.POST.get('info', '')

    group_profiles = GroupProfile.objects.all().order_by('-id')
    if info:
        group_profiles = group_profiles.filter(
            Q(group__name__icontains=info)
            | Q(desc__icontains=info)
            | Q(remark__icontains=info))

    group_dict_list = []
    for g in group_profiles:
        group_dict = {
            'id': g.id,
            'name': g.group.name,
            'desc': g.desc,
            'remark': g.remark
        }
        group_dict_list.append(group_dict)

    status = True

    res['status'] = status
    res['groups'] = group_dict_list

    return json_response(res)


@login_required
@rights_required('group_create')
def admin_group_create(request):
    """管理员创建角色"""
    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    name = request.POST.get('name', '')
    desc = request.POST.get('desc', '')
    remark = request.POST.get('remark', '')

    perm_list = request.POST.getlist('perm_list', [])

    try:

        if not name:
            msg = af.GROUP_NAME_EMPTYf
            assert False

        group, is_new = Group.objects.get_or_create(name=name)

        if not is_new:
            msg = af.GROUP_ALREADY_EXIST
            assert False

        creator_username = request.user.username
        group_profile, _ = GroupProfile.objects.get_or_create(group=group)
        group_profile.creator_name = creator_username
        group_profile.desc = desc
        group_profile.remark = remark
        group_profile.save()

        if perm_list:
            for perm_id in perm_list:
                PermGroup.assign_perm(perm_id, group)

        log_msg = om.CREATE_GROUP % (creator_username, name)
        OperateLog.write_operate_log(request, om.ACCOUNTS, log_msg)

        status = True

    except AssertionError:
        res['msg'] = msg

    res['status'] = status

    return json_response(res)


@login_required
@rights_required('group_create')
def admin_group_edit(request):
    """管理员修改角色"""
    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    group_id = request.POST.get('group_id', '')
    desc = request.POST.get('desc', '')
    remark = request.POST.get('remark', '')

    perm_list = request.POST.getlist('perm_list', [])

    try:

        group_profile = GroupProfile.objects.filter(id=group_id)

        if not group_profile:
            msg = af.GROUP_EMPTY
            assert False

        group = group_profile.group

        creator_username = request.user.username
        group_profile.desc = desc
        group_profile.remark = remark
        group_profile.save()

        if perm_list:

            group_perm = PermGroup.objects.filter(group=group)
            group_perm.delete()

            for perm_id in perm_list:
                PermGroup.assign_perm(perm_id, group)

        log_msg = om.EDIT_GROUP % (creator_username, group.name)
        OperateLog.write_operate_log(request, om.ACCOUNTS, log_msg)

        status = True

    except AssertionError:
        res['msg'] = msg

    res['status'] = status

    return json_response(res)
