
import json
import datetime

from django.db.models import Q
from django.contrib.auth.models import Group
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required


from base.functions import create_user
from common.decorators import rights_required
from common.feed import (AccountsFeed as af, OperateMsg as om, APIUrl,
                         SecWafConf as sf)
from common.functions import (json_response, int_check, PAGE_SIZE,
                              get_pagination, timestamp_to_datetime,
                              data_pagination, datetime_to_str, handle_req_time,
                              handle_request_user)
from common.fusion_api.cc_api import ChinaCacheAPI
from base.models import (UserProfile, OperateLog, GroupProfile, PermUser,
                         PermGroup, Strategy, Product)
from base.ajax.base_ajax import (set_user_api_status, user_open_parent_api,
                                 set_user_api_remove)


@login_required
@rights_required('parent_create')
def admin_create_parent_user(request):
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
    linkman = request.POST.get('linkman', '')
    email = request.POST.get('email', '')
    mobile = request.POST.get('mobile', '')
    is_api = request.POST.get('is_api', '')
    is_active = request.POST.get('is_active', '1')
    perm_list = request.POST.getlist('perm[]', [])

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

        is_api = int(is_api)
        if is_api is None:
            msg = af.PARAM_ERROR
            assert False

        is_active = int_check(is_active)
        if is_active is None:
            msg = af.PARAM_ERROR
            assert False

    except AssertionError:
        res['msg'] = _(msg)
        return json_response(res)

    identity = 'is_parent'

    group = Group.objects.filter(id=GroupProfile.CUSTOMER_ID).first()

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
        'creator_username': creator_username,
        'is_api': True if is_api else False

    }

    user = create_user(**param)

    if not user:
        res['msg'] = _(af.PARAM_ERROR)
        return json_response(res)

    if not is_active:
        user.is_active = False
        user.save()

    for perm_code in perm_list:
        PermUser.assign_perm(perm_code, user)
        if perm_code == 'client_cdn_menu':
            cdn_product = Product.objects.filter(code='CDN').first()
            cdn_strategy = Strategy.get_obj_from_property(
                'CC', 'CDN', 'CDN')
            user.product_list.add(cdn_product)
            user.strategy_list.add(cdn_strategy)
            user.save()
        # elif perm_code == 'client_security_menu':
        #     sec_product = Product.objects.filter(code='SECURITY').first()
        #     sec_strategy = Strategy.get_obj_from_property(
        #         'QINGSONG', 'SECURITY', 'WAF')
        #     user.product_list.add(sec_product)
        #     user.strategy_list.add(sec_strategy)
        #     user.save()

    log_msg = om.CREATE_USER % (creator_username, identity, username)
    OperateLog.write_operate_log(request, om.ACCOUNTS, log_msg)

    status = True

    res['status'] = status

    return json_response(res)


@login_required
@rights_required('parent_create')
def admin_edit_parent_user(request):
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

    is_active = request.POST.get('is_active', '')

    password = request.POST.get('password', '')
    reset_password = request.POST.get('reset_password', '0')

    perm_list = request.POST.getlist('perm[]', [])

    try:

        check_user = UserProfile.objects.filter(username=username).first()
        if not check_user:
            msg = af.USER_NOT_EXIST
            assert False

        if is_active:
            is_active = int_check(is_active)
            if is_active is None:
                msg = af.PARAME_ERROR
                assert False

            check_user.is_active = True if is_active else False

        if password:
            check_user.set_password(password)

        if reset_password:
            reset_password = int_check(reset_password)
            check_user.reset_password = True if reset_password else False

    except AssertionError:
        res['msg'] = _(msg)
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

    user_perm, is_new = PermUser.objects.get_or_create(user=check_user)
    if is_new:
        user_perm.save()

    user_perm.perm.clear()
    # check_user.product_list.clear()
    # check_user.strategy_list.clear()

    for perm_code in perm_list:
        PermUser.assign_perm(perm_code, check_user)

        if perm_code == 'client_cdn_menu':
            cdn_product = Product.objects.filter(code='CDN').first()
            cdn_strategy = Strategy.get_obj_from_property(
                'CC', 'CDN', 'CDN')
            check_user.product_list.add(cdn_product)
            check_user.strategy_list.add(cdn_strategy)
            check_user.save()
        # elif perm_code == 'client_security_menu':
        #     sec_product = Product.objects.filter(code='SECURITY').first()
        #     sec_strategy = Strategy.get_obj_from_property(
        #         'QINGSONG', 'SECURITY', 'WAF')
        #     check_user.product_list.add(sec_product)
        #     check_user.strategy_list.add(sec_strategy)
        #     check_user.save()

    check_user.save()

    log_msg = om.EDIT_USER % (creator_username, username)
    OperateLog.write_operate_log(request, om.ACCOUNTS, log_msg)

    status = True

    res['status'] = status

    return json_response(res)


@login_required
@rights_required('parent_create')
def admin_open_parent_api(request):
    """管理员开启用户api功能"""
    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }
    creator = request.user

    try:
        user = handle_request_user(request)
        # user = UserProfile.objects.get(id=93)
        if not user:
            msg = af.USER_NOT_EXIST
            assert False

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

            log_msg = om.OPEN_API % (creator.username, user.username)
            OperateLog.write_operate_log(request, om.ACCOUNTS, log_msg)

            status = True

    except AssertionError:
        res['msg'] = _(msg)

    res['status'] = status
    print(res)

    return json_response(res)


@login_required
@rights_required('parent_create')
def admin_set_parent_api_status(request):
    """管理员设置父账号api状态"""
    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }
    creator = request.user

    try:
        user = handle_request_user(request)
        if not user:
            msg = af.USER_NOT_EXIST
            assert False

        msg = set_user_api_status(request, user)
        if msg:
            assert False

        log_msg = om.OPEN_SET_API_STATUS % (creator.username, user.username)
        OperateLog.write_operate_log(request, om.ACCOUNTS, log_msg)

        status = True

    except AssertionError:
        res['msg'] = _(msg)

    res['status'] = status

    return json_response(res)


@login_required
@rights_required('parent_create')
def admin_set_parent_api_remove(request):
    """管理员开启用户api功能"""
    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }
    creator = request.user

    try:
        user = handle_request_user(request)
        if not user:
            msg = af.USER_NOT_EXIST
            assert False

        msg = set_user_api_remove(user)

        if not msg:
            log_msg = om.REMOVE_API % (creator.username, user.username)
            OperateLog.write_operate_log(request, om.ACCOUNTS, log_msg)

            status = True

    except AssertionError:
        res['msg'] = _(msg)

    res['status'] = status
    print(res)

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
    group_id = request.POST.get('group_id', '')

    try:

        if not username:
            msg = af.USERNAME_EMPTY
            assert False

        check_user = UserProfile.objects.filter(username=username)
        if check_user:
            msg = af.USER_EXIST
            assert False

        group = Group.objects.filter(id=group_id).first()

    except AssertionError:
        res['msg'] = _(msg)
        return json_response(res)

    password = ''    # ldap 密码使用云密码
    identity = 'is_admin'

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
        res['msg'] = _(af.PARAM_ERROR)
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
    is_active = request.POST.get('is_active', '')

    try:

        if not username:
            msg = af.USERNAME_EMPTY
            assert False

        check_user = UserProfile.objects.filter(username=username).first()
        if not check_user:
            msg = af.USER_NOT_EXIST
            assert False

        if is_active:
            is_active = int_check(is_active)
            if is_active is None:
                msg = af.PARAME_ERROR
                assert False
            check_user.is_active = True if is_active else False

        if group_id:
            group = Group.objects.filter(id=group_id).first()
            if not group:
                msg = af.GROUP_EMPTY
                assert False

            check_user.groups.clear()
            check_user.groups.add(group)

        check_user.save()

    except AssertionError:
        res['msg'] = _(msg)
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

    user_list = UserProfile.objects.filter(**check_filter).order_by('-id')
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
        res['msg'] = _(msg)
        return json_response(res)

    if user_list:
        user_type = request.POST.get('user_type', '')

        if user_type == 'is_parent':
            user_list = user_list.filter(is_parent=True)
        elif user_type == 'is_agent':
            user_list = user_list.filter(is_agent=True)

    user_list = user_list.filter().exclude(
        is_child=True).order_by('is_active').order_by('-id')

    check_msg, user_list, pagination = data_pagination(request, user_list)

    if check_msg:
        res['msg'] = _(check_msg)
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
    group_id = request.POST.get('groups_id', '')
    if group_id:
        groups = Group.objects.filter(id=group_id)
        group_ids = [i.id for i in groups]
    else:
        admin_group = GroupProfile.group_views()
        group_ids = [i['group_id'] for i in admin_group]

    msg, user_list = _get_user_list(request, group_ids)

    if msg:
        res['msg'] = _(msg)
        return json_response(res)


    check_msg, user_list, pagination = data_pagination(request, user_list)

    if check_msg:
        res['msg'] = _(check_msg)
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

        msg, start_time, end_time = handle_req_time(start_time, end_time)
        if msg:
            assert False

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

    if msg:
        res['msg'] = _(msg)
        return json_response(res)

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

    if msg:
        res['msg'] = _(msg)
        return json_response(res)

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

    perm_list = request.POST.getlist('perm_list[]', [])

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
        res['msg'] = _(msg)

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

    perm_list = request.POST.getlist('perm_list[]', [])

    try:

        group_profile = GroupProfile.objects.filter(id=group_id).first()

        if not group_profile:
            msg = af.GROUP_EMPTY
            assert False

        group = group_profile.group

        creator_username = request.user.username
        group_profile.desc = desc
        group_profile.remark = remark
        group_profile.save()

        if perm_list:

            group_perm, is_new = PermGroup.objects.get_or_create(group=group)
            group_perm.perm.clear()
            for perm_id in perm_list:
                PermGroup.assign_perm(perm_id, group)

        log_msg = om.EDIT_GROUP % (creator_username, group.name)
        OperateLog.write_operate_log(request, om.ACCOUNTS, log_msg)

        status = True

    except AssertionError:
        res['msg'] = _(msg)

    res['status'] = status

    return json_response(res)


@login_required
@rights_required('group_create')
def admin_group_delete(request):
    """管理员删除角色"""
    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    obj_id = request.POST.get('obj_id', '')

    try:

        group_profile = GroupProfile.objects.filter(id=obj_id).first()

        if not group_profile:
            msg = af.GROUP_EMPTY
            assert False
        group = group_profile.group
        group_user = group.user_set.all()

        if group_user:
            msg = af.GROUP_HAS_USER
            assert False

        group_profile.group.delete()

        log_msg = om.DELETE_GROUP % (request.user.username, group.name)
        OperateLog.write_operate_log(request, om.ACCOUNTS, log_msg)
        status = True

    except AssertionError:
        res['msg'] = _(msg)

    res['status'] = status

    return json_response(res)


@login_required
@rights_required('bind_parent_CMS_views')
def admin_get_parent_cms_list(request):
    """获取cms用户信息"""
    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    username = request.POST.get('username', '')
    cms_username = request.POST.get('cms_username', '')

    try:

        parent_list = UserProfile.objects.all()

        if username:
            parent_list = parent_list.filter(username=username)

        username_list = [i.username for i in parent_list]

        body = {
            'username_list': username_list,
            'cms_username': cms_username
        }

        api_res = APIUrl.post_link('user_query', body)
        user_query = api_res.get('user_query', {})

        username_list = list(user_query.keys())

        user_list = UserProfile.objects.filter(username__in=username_list)

        user_dict_list = []

        for user in user_list:
            username = user.username

            cms_username = user_query[username].get('cms_username', '')
            if not cms_username:
                continue

            user_dict = {
                'id': user.id,
                'username': username,
                'company': user.company,
                'cms_username': cms_username
            }
            user_dict_list.append(user_dict)

        check_msg, user_list, pagination = data_pagination(
            request, user_dict_list)

        if check_msg:
            res['msg'] = check_msg
            return json_response(res)


        status = True

        res['status'] = status
        res['user_list'] = user_list
        res['page_info'] = pagination

    except AssertionError:
        res['msg'] = _(msg)

    res['status'] = status

    return json_response(res)


@login_required
@rights_required('bind_parent_CMS_views')
def admin_user_binding(request):
    """管理员绑定用户cms关系"""
    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    username = request.POST.get('username', '')
    cms_username = request.POST.get('cms_username', '')

    contract_list = request.POST.get('contract_list', '[]')
    contract_list = json.loads(contract_list)

    try:
        user = UserProfile.objects.filter(username=username).first()

        if not user:
            msg = af.USER_NOT_EXIST
            assert False

        contract_info_list = []
        for c in contract_list:

            contract_info = {
                'contract_name': c['contract_name'],
                'start_time': c['start_time'],
                'end_time': c['end_time'],
                'product_list': c['product_list']
            }

            contract_info_list.append(contract_info)

        cms_password = ChinaCacheAPI.get_cms_password(cms_username)

        body = {
            'user_id': user.id,
            'username': username,
            'cms_username': cms_username,
            'cms_password': cms_password,
            'contract_info': contract_info_list
        }

        res = APIUrl.post_link('user_binding_cms', body)
        result = res.get('result', False)

        if result:
            status = True

    except AssertionError:
        res['msg'] = _(msg)

    res['status'] = status

    return json_response(res)


@login_required
@rights_required('bind_parent_CMS_views')
def admin_user_relieve_binding(request):
    """管理员解除绑定用户cms关系"""
    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    username = request.POST.get('username', '')

    try:
        user = UserProfile.objects.filter(username=username).first()

        if not user:
            msg = af.USER_NOT_EXIST
            assert False

        body = {
            'username': username,
        }

        res = APIUrl.post_link('user_relieve_cms_binding', body)
        result = res.get('result', False)

        if result:
            status = True

    except AssertionError:
        res['msg'] = _(msg)

    res['status'] = status

    return json_response(res)


@login_required
@rights_required('bind_parent_CMS_views')
def admin_set_user_strategy_conf(request):
    """管理员绑定设置用户三方平台基础信息"""
    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }
    username = request.POST.get('username', '')
    provider = request.POST.get('provider', 'QINGSONG')
    product = request.POST.get('product', 'SECURITY')
    service = request.POST.get('service', 'WAF')
    value = request.POST.get('value', sf.BASE_TOKEN)

    try:
        user = UserProfile.objects.filter(username=username).first()

        if not user:
            msg = af.USER_NOT_EXIST
            assert False
        strategy = Strategy.get_obj_from_property(provider, product, service)
        key = strategy.code.lower()

        body = {
            'user_id': user.id,
            'username': username,
            'fields': {key: value},
        }

        res = APIUrl.post_link('update_user', body)
        return_code = res.get('return_code', 0)

        if return_code != 0:
            assert False

        status = True

    except AssertionError:
        res['msg'] = _(msg)

    res['status'] = status

    return json_response(res)


@login_required
@rights_required('bind_parent_CMS_views')
def admin_sync_contract_info(request):
    """管理员同步合同信息"""
    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    contract_name = request.POST.get('contract_name', '')
    username = request.POST.get('username', '')

    # contract_name = 'Microsoft-azure-1510（重录）-2'
    # username = 'test'

    try:
        user = UserProfile.objects.filter(username=username).first()

        if not user:
            msg = af.USER_NOT_EXIST
            assert False

        start_time, end_time, product_list = ChinaCacheAPI.get_contract_info(
            contract_name)

        now = datetime.datetime.now()
        now_str = datetime_to_str(now, _format='%Y-%m-%d')
        is_effective = True if start_time < now_str < end_time else False

        res['is_effective'] = is_effective
        res['start_time'] = start_time
        res['end_time'] = end_time
        res['product_list'] = product_list

        status = True

    except AssertionError:
        res['msg'] = _(msg)

    res['status'] = status

    return json_response(res)


@login_required
@rights_required('bind_parent_CMS_views')
def admin_binding_user_contract(request):
    """管理员绑定合同"""
    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    contract_name = request.POST.get('contract_name', '')
    start_time = request.POST.get('start_time', '')
    end_time = request.POST.get('end_time', '')
    product_list = request.POST.getlist('product_list[]', [])

    username = request.POST.get('username', '')

    # contract_name = 'Microsoft-azure-1510（重录）-2'
    # contract_name = 'jwcm-CC-201907'
    # username = 'test'
    # start_time = "2019-08-09"
    # end_time = "2019-10-08"
    # product_list = [{
    #     "product_name" : "http视频点播加速服务",
    #     "product_code" : "9010300000432"
    # }]

    try:
        user = UserProfile.objects.filter(username=username).first()

        if not user:
            msg = af.USER_NOT_EXIST
            assert False

        body = {
            'username': user.username,
            'contract': {
                contract_name: {
                    'start_time': start_time,
                    'end_time': end_time,
                    'product': product_list,
                }
            }
        }

        res = APIUrl.post_link('binding_user_contract', body)
        if res.get('return_code', 0) == 0:
            status = True

            log_msg = om.BINDING_USER_CONTRACT % (
                request.user.username, username, contract_name)
            OperateLog.write_operate_log(request, om.ACCOUNTS, log_msg)

    except AssertionError:
        res['msg'] = _(msg)

    res['status'] = status

    return json_response(res)


@login_required
@rights_required('bind_parent_CMS_views')
def admin_user_relieve_contract(request):
    """解除绑定合同"""

    msg = ''
    status = False

    res = {
        'status': status,
        'msg': msg
    }

    contract_name = request.POST.get('contract_name', '')
    username = request.POST.get('username', '')

    # contract_name = '20190808_TEST'
    # username = 'test'

    try:
        user = UserProfile.objects.filter(username=username).first()

        if not user:
            msg = af.USER_NOT_EXIST
            assert False

        body = {
            'username': user.username,
            'contract': contract_name
        }

        print(body)

        res = APIUrl.post_link('relieve_user_contract', body)
        if res.get('return_code', 0) == 0:
            status = True

            log_msg = om.BINDING_USER_CONTRACT % (
                request.user.username, username, contract_name)
            OperateLog.write_operate_log(request, om.ACCOUNTS, log_msg)

    except AssertionError:
        res['msg'] = _(msg)

    res['status'] = status

    return json_response(res)