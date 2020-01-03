

from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required


from common.feed import AccountsFeed as af, APIUrl
from base.models import GroupProfile, UserProfile, Perm, PermUser, PermGroup
from common.decorators import rights_required
from base.functions import handle_perm
from common.functions import timestamp_to_str


@login_required
@rights_required('parent_create')
def create_parent_user_views(request):
    """管理员创建父账号"""
    all_perm = Perm.objects.filter(content_type__contains='CLIENT')

    perm = {}
    perm_type = []

    menu_level_1_list = all_perm.filter(level=1)

    user_type = [
        {
            'id': 'is_parent',
            'name': af.COMMON_CUSTOMER
        },
        {
            'id': 'is_agent',
            'name': af.AGENT_CUSTOMER
        }
    ]

    for i in menu_level_1_list:

        type_dict = {
            'id': i.code,
            'name': i.type_name
        }

        perm_type.append(type_dict)

        p_perm_query = all_perm.filter(parent_code=i.code)
        p_perm = [
            {'id': i.code, 'name': i.name} for i in p_perm_query
        ]
        perm[i.code] = p_perm

    res = {
        'user_type': user_type,
        'perm': perm,
        'perm_type': perm_type
    }

    return render(request, 'user_accounts/create_parent_user.html', res)


@login_required
@rights_required('all_parent_views')
def admin_parent_list_views(request):
    """管理员获取父账号用户列表"""

    user_type = [
        {
            'id': 'is_parent',
            'name': af.COMMON_CUSTOMER
        },
        {
            'id': 'is_agent',
            'name': af.AGENT_CUSTOMER
        }
    ]
    res = {
        'user_type': user_type,
    }

    return render(request, 'user_accounts/admin_parent_list_views.html', res)


@login_required
@rights_required('all_parent_views')
def admin_parent_details_views(request, user_id):
    """管理员获取父账号用户详情"""

    client = UserProfile.objects.filter(id=user_id).first()

    group = client.groups.first()
    client.group_name = group

    user_perm_code_list = PermUser.user_perm(client)

    user_perm_list = Perm.objects.filter(code__in=user_perm_code_list)
    user_perm, user_perm_type = handle_perm(user_perm_list)

    all_perm = Perm.objects.filter(content_type__contains='CLIENT')
    all_perm, all_perm_type = handle_perm(all_perm)

    client.company = client.company if client.company else ''
    client.mobile = client.mobile if client.mobile else ''
    client.active_type = af.IS_ACTIVE if client.is_active else af.IS_NOT_ACTIVE

    body = {
        'username_list': [client.username]
    }

    res = APIUrl.post_link('user_query', body)
    user_query = res.get('user_query', {})
    user_info = user_query.get(client.username, {})

    secret_id = user_info.get('api_secret_id', '')
    secret_key = user_info.get('api_secret_key', '')
    api_create_time = user_info.get('api_create_time', '')
    if api_create_time:
        api_create_time = timestamp_to_str(api_create_time)
    api_open = user_info.get('api_open', 0)

    api_info = list()

    if secret_id and secret_key:
        api_info_dict = {
            'secret_id': secret_id,
            'secret_key': secret_key,
            'create_time': api_create_time,
            'status': api_open,
            'type': _(af.COMMON)
        }
        api_info.append(api_info_dict)

    client.api_info = api_info

    res = {
        'client': client,
        'user_perm': user_perm,
        'user_perm_type': user_perm_type,

        'all_perm': all_perm,
        'all_perm_type': all_perm_type
    }

    return render(request, 'user_accounts/admin_parent_details_views.html', res)


@login_required
@rights_required('all_parent_opt_log_views')
def admin_parent_opt_log_views(request):
    """管理员获取父账号操作记录"""

    res = {
    }

    return render(request, 'user_accounts/admin_parent_opt_log.html', res)


@login_required
@rights_required('bind_parent_CMS_views')
def admin_bind_cms_parent_views(request):
    """管理员绑定cms账号"""
    res = {
    }

    return render(request, 'user_accounts/admin_bind_cms_parent.html', res)


@login_required
@rights_required('all_admin_views')
def admin_admin_list_views(request):
    """管理员获取管理员账号列表"""

    res = {
        'group_type': GroupProfile.group_views(),
    }

    return render(request, 'admin_accounts/admin_admin_list_views.html', res)


@login_required
@rights_required('admin_create')
def create_admin_user_views(request):
    """管理员创建管理员账号"""

    res = {
        'group_type': GroupProfile.group_views(),
    }

    return render(request, 'admin_accounts/create_admin_user.html', res)


@login_required
@rights_required('all_admin_views')
def admin_admin_details_views(request, user_id):
    """管理员获取管理账号用户详情"""

    client = UserProfile.objects.filter(id=user_id).first()

    group = client.groups.first()
    client.group_name = group.name

    res = {
        'client': client,
        'group_type': GroupProfile.group_views(),
    }

    return render(request, 'admin_accounts/admin_admin_details_views.html', res)


@login_required
@rights_required('all_admin_opt_log_views')
def admin_admin_opt_log_views(request):
    """管理员获取管理员操作记录"""

    res = {
    }
    return render(request, 'admin_accounts/admin_admin_opt_log_views.html', res)


@login_required
@rights_required('group_manage')
def admin_group_manage_views(request):
    """管理员角色管理页面"""

    res = {
    }

    return render(request, 'admin_accounts/admin_group_manage_views.html', res)


@login_required
@rights_required('group_create')
def admin_group_create_views(request):
    """管理员角色创建"""

    all_perm = Perm.objects.all()

    perm, perm_type = handle_perm(all_perm)

    res = {
        'perm': perm,
        'perm_type': perm_type
    }
    return render(request, 'admin_accounts/admin_group_create_views.html', res)


@login_required
@rights_required('group_manage')
def admin_group_details_views(request, group_id):
    """管理员获取角色用户详情"""

    group_profile = GroupProfile.objects.filter(id=group_id).first()

    perm_group = PermGroup.objects.filter(group=group_profile.group).first()
    group_perm = {}
    group_perm_type = []
    if perm_group and perm_group.perm.all():
        group_perm, group_perm_type = handle_perm(perm_group.perm.all())

    all_perm = Perm.objects.filter(content_type__contains='ADMIN')
    all_perm, all_perm_type = handle_perm(all_perm)

    res = {
        'group_perm': group_perm,
        'group_perm_type': group_perm_type,
        'group_profile': group_profile,

        'all_perm': all_perm,
        'all_perm_type': all_perm_type
    }

    return render(request, 'admin_accounts/admin_group_details_views.html', res)


@login_required
@rights_required('bind_parent_CMS_views')
def admin_create_binding_views(request):
    """管理员cms客户绑定关系"""

    parent_list = UserProfile.objects.filter(is_parent=True)

    body = {
        'username_list': [user.username for user in parent_list]
    }

    api_res = APIUrl.post_link('user_query', body)
    user_query = api_res.get('user_query', {})

    parent_dict_list = []
    for parent in parent_list:
        username = parent.username

        user_info = user_query.get(username, {})

        cms_username = user_info.get('cms_username', '')
        if cms_username:
            continue

        parent_info = {
            'username': username,
            'user_id': parent.id,
            'type_name': parent.type_name,
            'is_active': 1 if parent.is_active else 0,
            'company': parent.company,
        }
        parent_dict_list.append(parent_info)

    res = {
        'property': 'is_create',
        'user_list': parent_dict_list
    }
    return render(request, 'user_accounts/create_binding.html', res)


@login_required
@rights_required('bind_parent_CMS_views')
def admin_cms_details_views(request, user_id):
    """管理员cms客户绑定关系详情"""

    res = {
        'property': 'is_details'
    }

    client = UserProfile.objects.filter(id=user_id).first()

    if client:
        username = client.username

        body = {
            'username_list': [username],
        }

        api_res = APIUrl.post_link('user_query', body)
        user_query = api_res.get('user_query', {})

        cms_username = user_query.get(username, {}).get('cms_username', '')
        contract = user_query.get(username, {}).get('contract', '')

        client.cms_username = cms_username
        client.user_id = str(user_id)
        client.company = '' if not client.company else client.company

        res['client'] = client
        res['contract'] = contract

    return render(request, 'user_accounts/create_binding.html', res)


@login_required
@rights_required('bind_parent_CMS_views')
def admin_set_user_strategy_views(request, user_id):
    """父账号安全域名配置页面"""
    client = UserProfile.objects.filter(id=user_id).first()

    res = {
        'client': client,
    }
    return render(request, 'safe_cdn/safe_cdn_configure.html', res)




